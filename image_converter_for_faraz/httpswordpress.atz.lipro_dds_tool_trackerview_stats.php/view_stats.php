<?php
header('Content-Type: text/html; charset=utf-8');

function get_geo_data($ip) {
    try {
        $url = "http://ip-api.com/json/" . $ip;
        $response = file_get_contents($url);
        return json_decode($response, true);
    } catch (Exception $e) {
        return null;
    }
}

try {
    $db = new PDO('mysql:host=localhost;dbname=wordpres_test', 'wordpres_test', '$$$Pro381998');
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Basic stats
    $stats = [
        'total_users' => $db->query("SELECT COUNT(DISTINCT user_id) FROM users")->fetchColumn(),
        'active_today' => $db->query("SELECT COUNT(DISTINCT user_id) FROM users WHERE last_seen >= DATE_SUB(NOW(), INTERVAL 24 HOUR)")->fetchColumn(),
        'total_conversions' => $db->query("SELECT COUNT(*) FROM usage_stats WHERE event_type = 'conversion'")->fetchColumn(),
        'total_events' => $db->query("SELECT COUNT(*) FROM usage_stats")->fetchColumn()
    ];
    
    // Get user details with trial info
    $users = $db->query("
        SELECT 
            u.user_id,
            MIN(us.created_at) as first_seen,
            MAX(u.last_seen) as last_seen,
            u.total_uses,
            COUNT(us.id) as total_events,
            MAX(CASE WHEN us.event_type = 'startup' THEN us.created_at END) as last_startup,
            GROUP_CONCAT(DISTINCT us.system_info) as systems_used,
            GROUP_CONCAT(DISTINCT us.version) as versions_used
        FROM users u
        LEFT JOIN usage_stats us ON u.user_id = us.user_id
        GROUP BY u.user_id
        ORDER BY u.last_seen DESC
        LIMIT 100
    ")->fetchAll(PDO::FETCH_ASSOC);
    
    // Get recent activity
    $recent = $db->query("
        SELECT 
            DATE(created_at) as date, 
            COUNT(*) as events,
            COUNT(DISTINCT user_id) as unique_users,
            GROUP_CONCAT(DISTINCT event_type) as event_types
        FROM usage_stats
        GROUP BY DATE(created_at)
        ORDER BY date DESC
        LIMIT 7
    ")->fetchAll(PDO::FETCH_ASSOC);
    
    // Get event breakdown
    $events = $db->query("
        SELECT 
            event_type, 
            COUNT(*) as count,
            COUNT(DISTINCT user_id) as unique_users,
            MIN(created_at) as first_seen,
            MAX(created_at) as last_seen
        FROM usage_stats
        GROUP BY event_type
        ORDER BY count DESC
    ")->fetchAll(PDO::FETCH_ASSOC);
    
    // Get system statistics
    $systems = $db->query("
        SELECT 
            system_info,
            COUNT(DISTINCT user_id) as users,
            COUNT(*) as events
        FROM usage_stats 
        WHERE system_info IS NOT NULL
        GROUP BY system_info
        ORDER BY users DESC
    ")->fetchAll(PDO::FETCH_ASSOC);
    
    // Get location statistics
    $location_stats = $db->query("
        SELECT 
            COALESCE(country, 'Unknown') as country,
            COUNT(DISTINCT user_id) as unique_users,
            COUNT(*) as total_events,
            GROUP_CONCAT(DISTINCT city) as cities
        FROM usage_stats
        GROUP BY country
        ORDER BY unique_users DESC
    ")->fetchAll(PDO::FETCH_ASSOC);
    
    // Get recent connections with location
    $recent_connections = $db->query("
        SELECT 
            us.user_id,
            us.created_at,
            us.event_type,
            us.ip_address,
            us.country,
            us.region,
            us.city,
            us.system_info
        FROM usage_stats us
        WHERE us.ip_address IS NOT NULL
        ORDER BY us.created_at DESC
        LIMIT 20
    ")->fetchAll(PDO::FETCH_ASSOC);

    ?>
    <!DOCTYPE html>
    <html>
    <head>
        <title>DDS Converter Usage Statistics</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f8f9fa; }
            .stats-container { max-width: 1200px; margin: 0 auto; }
            .stat-box { 
                background: #fff; 
                padding: 20px; 
                margin: 10px 0; 
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            table { 
                width: 100%; 
                border-collapse: collapse; 
                margin: 15px 0; 
                background: #fff;
            }
            th, td { 
                padding: 12px 8px; 
                border: 1px solid #e9ecef; 
                text-align: left; 
            }
            th { background: #f8f9fa; font-weight: bold; }
            tr:hover { background: #f8f9fa; }
            .status-active { color: #28a745; }
            .status-inactive { color: #dc3545; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
            .location-info {
                display: flex;
                gap: 20px;
                margin-bottom: 10px;
            }
            .location-card {
                background: #fff;
                padding: 15px;
                border-radius: 4px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                flex: 1;
            }
            .map-container {
                height: 300px;
                margin: 20px 0;
                border-radius: 8px;
                overflow: hidden;
            }
        </style>
    </head>
    <body>
        <div class="stats-container">
            <h1>DDS Converter Usage Statistics</h1>
            
            <div class="stat-box">
                <h2>Overall Statistics</h2>
                <div class="grid">
                    <div>
                        <p>Total Users: <strong><?= $stats['total_users'] ?></strong></p>
                        <p>Active Users (24h): <strong><?= $stats['active_today'] ?></strong></p>
                    </div>
                    <div>
                        <p>Total Conversions: <strong><?= $stats['total_conversions'] ?></strong></p>
                        <p>Total Events: <strong><?= $stats['total_events'] ?></strong></p>
                    </div>
                </div>
            </div>
            
            <div class="stat-box">
                <h2>Recent Activity (Last 7 Days)</h2>
                <table>
                    <tr>
                        <th>Date</th>
                        <th>Events</th>
                        <th>Unique Users</th>
                        <th>Event Types</th>
                    </tr>
                    <?php foreach ($recent as $day): ?>
                    <tr>
                        <td><?= $day['date'] ?></td>
                        <td><?= $day['events'] ?></td>
                        <td><?= $day['unique_users'] ?></td>
                        <td><?= $day['event_types'] ?></td>
                    </tr>
                    <?php endforeach; ?>
                </table>
            </div>
            
            <div class="stat-box">
                <h2>Active Users</h2>
                <table>
                    <tr>
                        <th>User ID</th>
                        <th>First Seen</th>
                        <th>Last Seen</th>
                        <th>Total Uses</th>
                        <th>Events</th>
                        <th>Systems</th>
                        <th>Status</th>
                    </tr>
                    <?php foreach ($users as $user): 
                        $last_seen = strtotime($user['last_seen']);
                        $is_active = (time() - $last_seen) < (24 * 3600);
                        $trial_start = strtotime($user['first_seen']);
                        $trial_end = $trial_start + (7 * 24 * 3600);
                        $trial_remaining = $trial_end - time();
                    ?>
                    <tr>
                        <td><?= htmlspecialchars($user['user_id']) ?></td>
                        <td><?= $user['first_seen'] ?></td>
                        <td><?= $user['last_seen'] ?></td>
                        <td><?= $user['total_uses'] ?></td>
                        <td><?= $user['total_events'] ?></td>
                        <td><?= htmlspecialchars($user['systems_used']) ?></td>
                        <td>
                            <span class="<?= $is_active ? 'status-active' : 'status-inactive' ?>">
                                <?= $is_active ? '● Active' : '○ Inactive' ?>
                            </span>
                            <?php if ($trial_remaining > 0): ?>
                                <br>
                                <small>Trial: <?= round($trial_remaining/86400) ?> days left</small>
                            <?php endif; ?>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </table>
            </div>
            
            <div class="stat-box">
                <h2>Event Types</h2>
                <table>
                    <tr>
                        <th>Event</th>
                        <th>Count</th>
                        <th>Unique Users</th>
                        <th>First Seen</th>
                        <th>Last Seen</th>
                    </tr>
                    <?php foreach ($events as $event): ?>
                    <tr>
                        <td><?= htmlspecialchars($event['event_type']) ?></td>
                        <td><?= $event['count'] ?></td>
                        <td><?= $event['unique_users'] ?></td>
                        <td><?= $event['first_seen'] ?></td>
                        <td><?= $event['last_seen'] ?></td>
                    </tr>
                    <?php endforeach; ?>
                </table>
            </div>
            
            <div class="stat-box">
                <h2>System Usage</h2>
                <table>
                    <tr>
                        <th>System</th>
                        <th>Users</th>
                        <th>Events</th>
                    </tr>
                    <?php foreach ($systems as $system): ?>
                    <tr>
                        <td><?= htmlspecialchars($system['system_info']) ?></td>
                        <td><?= $system['users'] ?></td>
                        <td><?= $system['events'] ?></td>
                    </tr>
                    <?php endforeach; ?>
                </table>
            </div>

            <div class="stat-box">
                <h2>Geographic Distribution</h2>
                <table>
                    <tr>
                        <th>Country</th>
                        <th>Users</th>
                        <th>Events</th>
                        <th>Cities</th>
                    </tr>
                    <?php foreach ($location_stats as $loc): ?>
                    <tr>
                        <td><?= htmlspecialchars($loc['country']) ?></td>
                        <td><?= $loc['unique_users'] ?></td>
                        <td><?= $loc['total_events'] ?></td>
                        <td><?= htmlspecialchars($loc['cities']) ?></td>
                    </tr>
                    <?php endforeach; ?>
                </table>
            </div>

            <div class="stat-box">
                <h2>Recent Connections</h2>
                <table>
                    <tr>
                        <th>Time</th>
                        <th>User ID</th>
                        <th>Event</th>
                        <th>Location</th>
                        <th>System</th>
                    </tr>
                    <?php foreach ($recent_connections as $conn): ?>
                    <tr>
                        <td><?= $conn['created_at'] ?></td>
                        <td><?= htmlspecialchars(substr($conn['user_id'], 0, 8)) ?>...</td>
                        <td><?= htmlspecialchars($conn['event_type']) ?></td>
                        <td>
                            <?php if ($conn['country']): ?>
                                <?= htmlspecialchars($conn['city'] ? "{$conn['city']}, " : "") ?>
                                <?= htmlspecialchars($conn['country']) ?>
                            <?php else: ?>
                                Unknown
                            <?php endif; ?>
                        </td>
                        <td><?= htmlspecialchars($conn['system_info']) ?></td>
                    </tr>
                    <?php endforeach; ?>
                </table>
            </div>
        </div>
    </body>
    </html>
    <?php
    
} catch (PDOException $e) {
    die("Database error: " . $e->getMessage());
}