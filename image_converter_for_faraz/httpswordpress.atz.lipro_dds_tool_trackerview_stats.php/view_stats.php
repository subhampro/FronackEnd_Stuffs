<?php
header('Content-Type: text/html; charset=utf-8');

try {
    $db = new PDO('mysql:host=localhost;dbname=wordpres_test', 'wordpres_test', '$$$Pro381998');
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    $stats = [
        'total_users' => $db->query("SELECT COUNT(DISTINCT user_id) FROM users")->fetchColumn(),
        'active_today' => $db->query("SELECT COUNT(DISTINCT user_id) FROM users WHERE last_seen >= DATE_SUB(NOW(), INTERVAL 24 HOUR)")->fetchColumn(),
        'total_conversions' => $db->query("SELECT COUNT(*) FROM usage_stats WHERE event_type = 'conversion'")->fetchColumn()
    ];
    
    $recent = $db->query("
        SELECT DATE(created_at) as date, 
               COUNT(*) as events,
               COUNT(DISTINCT user_id) as unique_users
        FROM usage_stats
        GROUP BY DATE(created_at)
        ORDER BY date DESC
        LIMIT 7
    ")->fetchAll(PDO::FETCH_ASSOC);
    
    $events = $db->query("
        SELECT event_type, COUNT(*) as count
        FROM usage_stats
        GROUP BY event_type
        ORDER BY count DESC
    ")->fetchAll(PDO::FETCH_ASSOC);
    
    ?>
    <!DOCTYPE html>
    <html>
    <head>
        <title>DDS Converter Usage Statistics</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .stats-container { max-width: 800px; margin: 0 auto; }
            .stat-box { 
                background: #f5f5f5; 
                padding: 20px; 
                margin: 10px 0; 
                border-radius: 5px;
            }
            table { 
                width: 100%; 
                border-collapse: collapse; 
                margin: 15px 0; 
            }
            th, td { 
                padding: 8px; 
                border: 1px solid #ddd; 
                text-align: left; 
            }
            th { background: #f0f0f0; }
        </style>
    </head>
    <body>
        <div class="stats-container">
            <h1>DDS Converter Usage Statistics</h1>
            
            <div class="stat-box">
                <h2>Overall Statistics</h2>
                <p>Total Users: <?= $stats['total_users'] ?></p>
                <p>Active Users (24h): <?= $stats['active_today'] ?></p>
                <p>Total Conversions: <?= $stats['total_conversions'] ?></p>
            </div>
            
            <div class="stat-box">
                <h2>Recent Activity (Last 7 Days)</h2>
                <table>
                    <tr>
                        <th>Date</th>
                        <th>Events</th>
                        <th>Unique Users</th>
                    </tr>
                    <?php foreach ($recent as $day): ?>
                    <tr>
                        <td><?= $day['date'] ?></td>
                        <td><?= $day['events'] ?></td>
                        <td><?= $day['unique_users'] ?></td>
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
                    </tr>
                    <?php foreach ($events as $event): ?>
                    <tr>
                        <td><?= htmlspecialchars($event['event_type']) ?></td>
                        <td><?= $event['count'] ?></td>
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