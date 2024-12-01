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

function safe_html($str) {
    // Fix null parameter warning by providing empty string default
    return htmlspecialchars($str ?? '', ENT_QUOTES, 'UTF-8');
}

try {
    $db = new PDO('mysql:host=localhost;dbname=wordpres_test', 'wordpres_test', '$$$Pro381998');
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Simplified stats query
    $stats = [
        'total_users' => $db->query("SELECT COUNT(DISTINCT user_id) FROM users")->fetchColumn(),
        'active_today' => $db->query("SELECT COUNT(DISTINCT user_id) FROM users WHERE last_seen >= DATE_SUB(NOW(), INTERVAL 24 HOUR)")->fetchColumn(),
        'total_conversions' => $db->query("SELECT COUNT(*) FROM usage_stats WHERE event_type = 'conversion'")->fetchColumn(),
        'total_events' => $db->query("SELECT COUNT(*) FROM usage_stats")->fetchColumn(),
        'active_licenses' => $db->query("SELECT COUNT(*) FROM licenses WHERE status = 'active'")->fetchColumn(),
        'trial_users' => $db->query("
            SELECT COUNT(DISTINCT u.user_id) 
            FROM users u 
            LEFT JOIN licenses l ON u.user_id = l.machine_id 
            WHERE l.id IS NULL AND DATEDIFF(NOW(), u.first_seen) <= 7
        ")->fetchColumn()
    ];
    
    // Simplified users query
    $users = $db->query("
        SELECT 
            u.user_id,
            MIN(us.created_at) as first_seen,
            MAX(u.last_seen) as last_seen,
            u.total_uses,
            COUNT(us.id) as total_events,
            GROUP_CONCAT(DISTINCT IFNULL(us.system_info, 'Unknown')) as systems_used,
            GROUP_CONCAT(DISTINCT IFNULL(us.version, 'Unknown')) as versions_used,
            GROUP_CONCAT(DISTINCT IFNULL(us.ip_address, 'Unknown')) as ip_addresses,
            GROUP_CONCAT(DISTINCT IFNULL(us.country, 'Unknown')) as countries,
            GROUP_CONCAT(DISTINCT IFNULL(us.city, 'Unknown')) as cities
        FROM users u
        LEFT JOIN usage_stats us ON u.user_id = us.user_id
        GROUP BY u.user_id
        ORDER BY u.last_seen DESC
        LIMIT 100
    ")->fetchAll(PDO::FETCH_ASSOC);
    
    // Simplified recent activity query
    $recent = $db->query("
        SELECT 
            DATE(created_at) as date, 
            COUNT(*) as events,
            COUNT(DISTINCT user_id) as unique_users,
            GROUP_CONCAT(DISTINCT event_type) as event_types
        FROM usage_stats
        WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        GROUP BY DATE(created_at)
        ORDER BY date DESC
    ")->fetchAll(PDO::FETCH_ASSOC);
    
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
    
    // Get geographic distribution
    $geo_stats = $db->query("
        SELECT 
            COALESCE(country, 'Unknown') as country,
            COUNT(DISTINCT user_id) as unique_users,
            COUNT(*) as total_events,
            GROUP_CONCAT(DISTINCT city ORDER BY city) as cities,
            GROUP_CONCAT(DISTINCT region ORDER BY region) as regions,
            GROUP_CONCAT(DISTINCT isp ORDER BY isp) as isps
        FROM usage_stats
        WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
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

    // Update the license status query
    $user_license_info = $db->query("
        SELECT 
            u.user_id,
            u.first_seen,
            u.last_seen,
            l.license_key,
            l.created_at as license_created,
            l.expires_at,
            l.status as license_status,
            CASE 
                WHEN l.id IS NOT NULL AND l.status = 'active' THEN 'Active'
                WHEN l.id IS NOT NULL AND l.status = 'expired' THEN 'Expired'
                WHEN l.id IS NULL AND TIMESTAMPDIFF(DAY, u.first_seen, NOW()) <= 7 THEN 'Trial'
                ELSE 'Expired'
            END as display_status,
            TIMESTAMPDIFF(SECOND, NOW(), COALESCE(l.expires_at, DATE_ADD(u.first_seen, INTERVAL 7 DAY))) as seconds_remaining
        FROM users u
        LEFT JOIN licenses l ON u.user_id = l.machine_id
        ORDER BY u.last_seen DESC
    ")->fetchAll(PDO::FETCH_ASSOC);

    foreach ($user_license_info as &$user) {
        $seconds_remaining = max(0, intval($user['seconds_remaining']));
        if ($seconds_remaining > 0) {
            $user['remaining'] = [
                'days' => floor($seconds_remaining / 86400),
                'hours' => floor(($seconds_remaining % 86400) / 3600),
                'minutes' => floor(($seconds_remaining % 3600) / 60)
            ];
        } else {
            $user['remaining'] = [
                'days' => 0,
                'hours' => 0,
                'minutes' => 0
            ];
        }
    }

    ?>
    <!DOCTYPE html>
    <html>
    <head>
        <title>DDS Converter Usage Statistics</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }
            .connection-details {
                font-size: 0.9em;
                margin-top: 10px;
                padding: 10px;
                background: #f8f9fa;
                border-radius: 4px;
            }
            .connection-item {
                display: flex;
                justify-content: space-between;
                padding: 5px 0;
                border-bottom: 1px solid #eee;
            }
            .status-badge {
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 0.8em;
            }
            .status-badge.active {
                background: #d4edda;
                color: #155724;
            }
            .status-badge.inactive {
                background: #f8d7da;
                color: #721c24;
            }
            .chart-container {
                position: relative;
                height: 300px;
                margin: 20px 0;
            }
            .status-trial {
                color: #ff9800;
                font-weight: bold;
            }
            .expiring-soon {
                color: #f44336;
                font-weight: bold;
                animation: blink 1s infinite;
            }
            @keyframes blink {
                50% { opacity: 0.5; }
            }
            .trial-badge {
                background: #ff9800;
                color: white;
                padding: 2px 6px;
                border-radius: 10px;
                font-size: 0.8em;
                margin-left: 5px;
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
                <div class="chart-container">
                    <canvas id="activityChart"></canvas>
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
                <?php foreach ($users as $user): 
                    $last_seen = strtotime($user['last_seen']);
                    $is_active = (time() - $last_seen) < (24 * 3600);
                    $trial_start = strtotime($user['first_seen']);
                    $trial_end = $trial_start + (7 * 24 * 3600);
                    $trial_remaining = $trial_end - time();
                    
                    // Remove connection history handling as it's not needed
                ?>
                <div class="user-panel">
                    <div class="user-header">
                        <h3>User ID: <?= safe_html(substr($user['user_id'], 0, 8)) ?>...</h3>
                        <span class="status-badge <?= $is_active ? 'active' : 'inactive' ?>">
                            <?= $is_active ? '● Active' : '○ Inactive' ?>
                        </span>
                    </div>
                    
                    <div class="user-info-grid">
                        <div class="info-block">
                            <h4>Activity Summary</h4>
                            <p>First Seen: <?= $user['first_seen'] ?></p>
                            <p>Last Seen: <?= $user['last_seen'] ?></p>
                            <p>Total Uses: <?= $user['total_uses'] ?></p>
                            <p>Events: <?= $user['total_events'] ?></p>
                        </div>
                    </div>
                </div>
                <?php endforeach; ?>
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
                        <td><?= safe_html($event['event_type']) ?></td>
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
                        <td><?= safe_html($system['system_info']) ?></td>
                        <td><?= $system['users'] ?></td>
                        <td><?= $system['events'] ?></td>
                    </tr>
                    <?php endforeach; ?>
                </table>
            </div>

            <div class="stat-box">
                <h2>Geographic Distribution</h2>
                <div class="chart-container">
                    <canvas id="geoChart"></canvas>
                </div>
                <table>
                    <tr>
                        <th>Country</th>
                        <th>Users</th>
                        <th>Events</th>
                        <th>Cities</th>
                    </tr>
                    <?php foreach ($geo_stats as $geo): ?>
                    <tr>
                        <td><?= safe_html($geo['country']) ?></td>
                        <td><?= $geo['unique_users'] ?></td>
                        <td><?= $geo['total_events'] ?></td>
                        <td><?= safe_html($geo['cities']) ?></td>
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
                        <td><?= safe_html(substr($conn['user_id'], 0, 8)) ?>...</td>
                        <td><?= safe_html($conn['event_type']) ?></td>
                        <td>
                            <?php if ($conn['country']): ?>
                                <?= safe_html($conn['city'] ? "{$conn['city']}, " : "") ?>
                                <?= safe_html($conn['country']) ?>
                            <?php else: ?>
                                Unknown
                            <?php endif; ?>
                        </td>
                        <td><?= safe_html($conn['system_info']) ?></td>
                    </tr>
                    <?php endforeach; ?>
                </table>
            </div>

            <!-- Replace the User License Status section with this updated version -->
            <div class="stat-box">
                <h2>User License Status</h2>
                <table>
                    <tr>
                        <th>User ID</th>
                        <th>Status</th>
                        <th>First Seen</th>
                        <th>Last Seen</th>
                        <th>Time Remaining</th>
                        <th>License Details</th>
                    </tr>
                    <?php foreach ($user_license_info as $user): 
                        $status_class = match($user['status'] ?? 'unknown') {
                            'licensed' => 'status-active',
                            'trial' => 'status-trial',
                            'expired', 'trial_expired' => 'status-inactive',
                            default => 'status-inactive'
                        };
                        
                        $remaining_text = '';
                        if (isset($user['status'])) {
                            if ($user['status'] === 'licensed') {
                                $remaining_text = ($user['days_remaining'] ?? 0) > 0 ? 
                                    "{$user['days_remaining']} days left" : "License expired";
                            } else if ($user['status'] === 'trial') {
                                $remaining_text = sprintf(
                                    "%d days, %d hours, %d minutes", 
                                    max(0, $user['days_remaining'] ?? 0),
                                    max(0, ($user['total_seconds_remaining'] ?? 0) % 86400 / 3600),
                                    max(0, ($user['total_seconds_remaining'] ?? 0) % 3600 / 60)
                                );
                            } else {
                                $remaining_text = $user['status'] === 'trial_expired' ? "Trial expired" : "License expired";
                            }
                        }
                        
                        $is_expiring_soon = (($user['days_remaining'] ?? 0) <= 2 && ($user['days_remaining'] ?? 0) > 0);
                    ?>
                    <tr>
                        <td><?= safe_html(substr($user['user_id'] ?? '', 0, 8)) ?>...</td>
                        <td>
                            <?php 
                            $status = $user['status'] ?? 'unknown';
                            $status_class = match($status) {
                                'licensed' => 'status-active',
                                'trial' => 'status-trial',
                                'expired', 'trial_expired' => 'status-inactive',
                                default => 'status-inactive'
                            };
                            ?>
                            <span class="<?= $status_class ?>">
                                <?= ucfirst($status) ?>
                                <?php if ($status === 'trial'): ?>
                                    <span class="trial-badge">Trial</span>
                                <?php endif; ?>
                            </span>
                        </td>
                        <td><?= $user['first_seen'] ?? 'N/A' ?></td>
                        <td><?= $user['last_seen'] ?? 'N/A' ?></td>
                        <td class="<?= (($user['days_remaining'] ?? 0) <= 2 && ($user['days_remaining'] ?? 0) > 0) ? 'expiring-soon' : '' ?>">
                            <?php 
                            if (isset($user['remaining'])) {
                                echo "{$user['remaining']['days']}d {$user['remaining']['hours']}h {$user['remaining']['minutes']}m";
                            } else {
                                echo "Expired";
                            }
                            ?>
                        </td>
                        <td>
                            <?php if (!empty($user['license_key'])): ?>
                                Key: •••<?= substr($user['license_key'], -4) ?><br>
                                Expires: <?= $user['expires_at'] ?? 'N/A' ?>
                            <?php else: ?>
                                No license
                            <?php endif; ?>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </table>
            </div>
        </div>
        
        <script>
            // Initialize charts with error handling
            const activityCtx = document.getElementById('activityChart').getContext('2d');
            const activityData = <?= json_encode(array_column($recent, 'events')) ?>;
            const activityLabels = <?= json_encode(array_column($recent, 'date')) ?>;
            
            if (activityData.length > 0) {
                new Chart(activityCtx, {
                    type: 'line',
                    data: {
                        labels: activityLabels,
                        datasets: [{
                            label: 'Events',
                            data: activityData,
                            borderColor: '#4CAF50'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false
                    }
                });
            }
            
            const geoCtx = document.getElementById('geoChart').getContext('2d');
            const geoData = <?= json_encode(array_column($geo_stats, 'unique_users')) ?>;
            const geoLabels = <?= json_encode(array_column($geo_stats, 'country')) ?>;
            
            if (geoData.length > 0) {
                new Chart(geoCtx, {
                    type: 'pie',
                    data: {
                        labels: geoLabels,
                        datasets: [{
                            data: geoData,
                            backgroundColor: ['#4CAF50', '#2196F3', '#FFC107', '#9C27B0', '#F44336']
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false
                    }
                });
            }
        </script>
    </body>
    </html>
    <?php
    
} catch (PDOException $e) {
    error_log("Database error: " . $e->getMessage());
    die("Database error occurred. Please check the error logs.");
}