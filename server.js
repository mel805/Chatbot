// ULTRA COMPLETE BAG Bot Dashboard Backend
const express = require('express');
const cors = require('cors');
const path = require('path');
const { Client: SSHClient } = require('ssh2');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors({ origin: '*' }));
app.use(express.json({ limit: '50mb' }));

const BOT_HOST = process.env.BOT_HOST || '82.67.65.98';
const BOT_PORT = parseInt(process.env.BOT_PORT) || 22222;
const BOT_USER = process.env.BOT_USER || 'bagbot';
const BOT_PASS = process.env.BOT_PASS || 'bagbot';
const BOT_BASE = process.env.BOT_BASE || '/home/bagbot/Bag-bot';
const DEFAULT_GUILD_ID = process.env.DASHBOARD_GUILD_ID || '1360897918504271882';

async function executeSSH(command) {
  return new Promise((resolve, reject) => {
    const conn = new SSHClient();
    let output = '';
    conn.on('ready', () => {
      conn.exec(command, (err, stream) => {
        if (err) { conn.end(); return reject(err); }
        stream.on('close', () => { conn.end(); resolve(output); })
              .on('data', (data) => { output += data.toString(); });
      });
    }).on('error', reject).connect({
      host: BOT_HOST, port: BOT_PORT, username: BOT_USER, password: BOT_PASS, readyTimeout: 30000
    });
  });
}

async function readBotConfig() {
  try {
    const output = await executeSSH(`cat ${BOT_BASE}/data/config.json`);
    return JSON.parse(output || '{}');
  } catch (e) { return { guilds: {} }; }
}

async function writeBotConfig(config) {
  const jsonStr = JSON.stringify(config, null, 2);
  await executeSSH(`cat > /tmp/cfg.json << 'EOF'\n${jsonStr}\nEOF && mv /tmp/cfg.json ${BOT_BASE}/data/config.json`);
}

async function readBotEnv() {
  try {
    const output = await executeSSH(`cat ${BOT_BASE}/.env`);
    const env = {};
    output.split('\n').forEach(line => {
      const trimmed = line.trim();
      if (trimmed && !trimmed.startsWith('#') && trimmed.includes('=')) {
        const idx = trimmed.indexOf('=');
        env[trimmed.slice(0, idx).trim()] = trimmed.slice(idx + 1).trim();
      }
    });
    return env;
  } catch (e) { return {}; }
}

// RESOLVE IDS TO NAMES
app.post('/api/resolve/users', async (req, res) => {
  try {
    const { userIds, guildId } = req.body;
    const env = await readBotEnv();
    const token = env.DISCORD_TOKEN;
    const base = 'https://discord.com/api/v10';
    const headers = { 'Authorization': `Bot ${token}` };
    
    const resolved = {};
    for (const userId of userIds.slice(0, 100)) { // Limit batch
      try {
        const response = await fetch(`${base}/guilds/${guildId}/members/${userId}`, { headers });
        if (response.ok) {
          const member = await response.json();
          resolved[userId] = {
            username: member.user.username,
            discriminator: member.user.discriminator,
            nickname: member.nick || member.user.global_name || member.user.username,
            avatar: member.user.avatar ? `https://cdn.discordapp.com/avatars/${userId}/${member.user.avatar}.png` : null
          };
        } else {
          resolved[userId] = { username: `User-${userId.slice(-4)}`, nickname: `User-${userId.slice(-4)}` };
        }
      } catch (e) {
        resolved[userId] = { username: `User-${userId.slice(-4)}`, nickname: `User-${userId.slice(-4)}` };
      }
    }
    res.json({ resolved });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// GET GUILD INFO WITH COUNTS
app.get('/api/discord/meta', async (req, res) => {
  try {
    const guildId = req.query.guildId || DEFAULT_GUILD_ID;
    const env = await readBotEnv();
    const token = env.DISCORD_TOKEN;
    const base = 'https://discord.com/api/v10';
    const headers = { 'Authorization': `Bot ${token}` };
    
    const [guildRes, channelsRes, rolesRes] = await Promise.all([
      fetch(`${base}/guilds/${guildId}?with_counts=true`, { headers }), // IMPORTANT: with_counts
      fetch(`${base}/guilds/${guildId}/channels`, { headers }),
      fetch(`${base}/guilds/${guildId}/roles`, { headers })
    ]);
    
    const [guild, channels, roles] = await Promise.all([
      guildRes.json(), channelsRes.json(), rolesRes.json()
    ]);
    
    res.json({
      guild: {
        id: guild.id,
        name: guild.name,
        icon: guild.icon ? `https://cdn.discordapp.com/icons/${guildId}/${guild.icon}.png` : null,
        memberCount: guild.approximate_member_count || guild.member_count || 0
      },
      channels: channels.map(ch => ({ id: ch.id, name: ch.name, type: ch.type, parentId: ch.parent_id })),
      roles: roles.map(r => ({ id: r.id, name: r.name, color: r.color }))
    });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});



// GET DISCORD CHANNELS (from cache file)
app.get('/api/discord/channels', async (req, res) => {
  try {
    const output = await executeSSH(`cat ${BOT_BASE}/data/discord-names.json`);
    const data = JSON.parse(output);
    res.json(data.channels || {});
  } catch (e) {
    console.error('[API] Error getting channels from cache:', e);
    res.json({}); // Return empty object on error
  }
});

// GET DISCORD ROLES (from cache file)
app.get('/api/discord/roles', async (req, res) => {
  try {
    const output = await executeSSH(`cat ${BOT_BASE}/data/discord-names.json`);
    const data = JSON.parse(output);
    res.json(data.roles || {});
  } catch (e) {
    console.error('[API] Error getting roles from cache:', e);
    res.json({}); // Return empty object on error
  }
});

// GET DISCORD MEMBERS (from cache file)
app.get('/api/discord/members', async (req, res) => {
  try {
    const output = await executeSSH(`cat ${BOT_BASE}/data/discord-names.json`);
    const data = JSON.parse(output);
    res.json(data.members || {});
  } catch (e) {
    console.error('[API] Error getting members from cache:', e);
    res.json({}); // Return empty object on error
  }
});

// GET STATS
app.get('/api/stats', async (req, res) => {
  try {
    const guildId = req.query.guildId || DEFAULT_GUILD_ID;
    const config = await readBotConfig();
    const guildConfig = config.guilds?.[guildId] || {};
    
    const psOutput = await executeSSH(`ps aux | grep 'node.*bot.js' | grep -v grep || echo ''`);
    const isRunning = psOutput.trim().length > 0;
    
    let uptime = 'N/A';
    if (isRunning) {
      const uptimeOutput = await executeSSH(`ps -o etime= -p $(pgrep -f 'node.*bot.js' | head -1) 2>/dev/null || echo '0'`);
      uptime = uptimeOutput.trim();
    }
    
    res.json({
      botRunning: isRunning,
      uptime,
      guildId,
      economyUsers: Object.keys(guildConfig.economy?.balances || {}).length,
      levelUsers: Object.keys(guildConfig.levels?.users || {}).length
    });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});


// GET FULL CONFIG (for dashboard loading)
app.get('/api/configs', async (req, res) => {
  try {
    const config = await readBotConfig();
    const guildId = req.query.guildId || DEFAULT_GUILD_ID;
    const guildConfig = config.guilds?.[guildId] || {};
    
    res.json({
      economy: guildConfig.economy || {},
      levels: guildConfig.levels || {},
      autokick: guildConfig.autokick || {},
      autothread: guildConfig.autothread || {},
      tickets: guildConfig.tickets || {},
      logs: guildConfig.logs || {},
      counting: guildConfig.counting || {},
      confess: guildConfig.confess || {},
      truthdare: guildConfig.truthdare || {},
      welcome: guildConfig.welcome || {},
      goodbye: guildConfig.goodbye || {},
      autoroles: guildConfig.autoroles || {},
      disboard: guildConfig.disboard || {},
      quarantine: guildConfig.quarantine || {},
      partners: guildConfig.partners || {}
    });
  } catch (e) {
    console.error('[API] Error getting configs:', e);
    res.status(500).json({ error: e.message });
  }
});
// GET ALL COMMANDS
app.get('/api/commands', async (req, res) => {
  try {
    const output = await executeSSH(`ls ${BOT_BASE}/src/commands/*.js | xargs -n1 basename | sed 's/.js$//' | sort`);
    const commands = output.trim().split('\n').filter(cmd => cmd.trim());
    res.json({ commands, count: commands.length });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// GET/UPDATE all config modules
const configModules = ['economy', 'levels', 'logs', 'tickets', 'truthdare', 'confess', 'autokick', 'counting', 'disboard', 'autothread', 'geo'];

configModules.forEach(module => {
  app.get(`/api/config/${module}`, async (req, res) => {
    try {
      const guildId = req.query.guildId || DEFAULT_GUILD_ID;
      const config = await readBotConfig();
      const data = config.guilds?.[guildId]?.[module] || {};
      res.json({ [module]: data });
    } catch (e) {
      res.status(500).json({ error: e.message });
    }
  });
  
  app.post(`/api/config/${module}`, async (req, res) => {
    try {
      const guildId = req.query.guildId || DEFAULT_GUILD_ID;
      const updates = req.body;
      const config = await readBotConfig();
      if (!config.guilds) config.guilds = {};
      if (!config.guilds[guildId]) config.guilds[guildId] = {};
      
      config.guilds[guildId][module] = { ...config.guilds[guildId][module], ...updates };
      await writeBotConfig(config);
      res.json({ success: true });
    } catch (e) {
      res.status(500).json({ error: e.message });
    }
  });
});

// BOT CONTROL
app.post('/api/bot/control', async (req, res) => {
  try {
    const { action } = req.body;
    const commands = {
      start: `cd ${BOT_BASE} && pm2 start src/bot.js --name bagbot`,
      stop: `pm2 stop bagbot`,
      restart: `pm2 restart bagbot`,
      deploy: `cd ${BOT_BASE} && node deploy-final.js`
    };
    const output = await executeSSH(commands[action] || commands.restart);
    res.json({ success: true, output });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// LOGS
app.get('/api/logs', async (req, res) => {
  try {
    const type = req.query.type || 'all';
    const lines = Math.min(500, parseInt(req.query.lines) || 100);
    const commands = {
      error: `tail -n ${lines} ~/.pm2/logs/bagbot-error.log 2>/dev/null || echo 'No logs'`,
      out: `tail -n ${lines} ~/.pm2/logs/bagbot-out.log 2>/dev/null || echo 'No logs'`,
      all: `pm2 logs bagbot --lines ${lines} --nostream 2>/dev/null || echo 'No logs'`
    };
    const output = await executeSSH(commands[type] || commands.all);
    res.json({ logs: output.split('\n') });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// BACKUPS
app.get('/api/backups', async (req, res) => {
  try {
    const output = await executeSSH(`ls -lth /var/data/backups/*.json 2>/dev/null | awk '{print $9, $5, $6, $7, $8}' || echo ''`);
    const backups = output.trim().split('\n').filter(l => l.trim()).map(line => {
      const parts = line.trim().split(/\s+/);
      return { filename: path.basename(parts[0]), size: parts[1] || '0', date: parts.slice(2).join(' ') };
    });
    res.json({ backups });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.post('/api/backup', async (req, res) => {
  try {
    const ts = new Date().toISOString().replace(/[:.]/g, '-');
    await executeSSH(`mkdir -p /var/data/backups && cp ${BOT_BASE}/data/config.json /var/data/backups/backup-${ts}.json`);
    res.json({ success: true, filename: `backup-${ts}.json` });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.post('/api/restore', async (req, res) => {
  try {
    const { filename } = req.body;
    await executeSSH(`cp /var/data/backups/${filename} ${BOT_BASE}/data/config.json`);
    res.json({ success: true });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// ============================================
// API ENDPOINT: INACTIVITY STATS
// ============================================
app.get('/api/inactivity/stats', async (req, res) => {
  try {
    const guildId = req.query.guildId || DEFAULT_GUILD_ID;
    const config = await readBotConfig();
    
    if (!config.guilds || !config.guilds[guildId]) {
      return res.json({ 
        enabled: false, 
        tracking: {}, 
        stats: { total: 0, inactive: 0, active: 0, warned: 0 }
      });
    }
    
    const autokick = config.guilds[guildId].autokick || {};
    const inactivityKick = autokick.inactivityKick || { enabled: false };
    const tracking = autokick.inactivityTracking || {};
    
    // Calculate stats
    const now = Date.now();
    const delayMs = (inactivityKick.delayDays || 30) * 24 * 60 * 60 * 1000;
    
    let stats = {
      total: Object.keys(tracking).length,
      inactive: 0,
      active: 0,
      warned: 0,
      plannedInactive: 0
    };
    
    const members = [];
    
    for (const [userId, data] of Object.entries(tracking)) {
      const lastActivity = data.lastActivity || 0;
      const inactiveDuration = now - lastActivity;
      const daysInactive = Math.floor(inactiveDuration / (24 * 60 * 60 * 1000));
      const isInactive = inactiveDuration > delayMs;
      const hasWarning = data.graceWarningUntil && data.graceWarningUntil > now;
      const isPlanned = data.plannedInactive && data.plannedInactive.until > now;
      
      if (isInactive) stats.inactive++;
      else stats.active++;
      
      if (hasWarning) stats.warned++;
      if (isPlanned) stats.plannedInactive++;
      
      members.push({
        userId,
        lastActivity,
        daysInactive,
        isInactive,
        hasWarning,
        isPlanned,
        plannedReason: isPlanned ? data.plannedInactive.reason : null,
        plannedUntil: isPlanned ? data.plannedInactive.until : null
      });
    }
    
    // Sort by most inactive first
    members.sort((a, b) => b.daysInactive - a.daysInactive);
    
    res.json({
      enabled: inactivityKick.enabled,
      config: {
        delayDays: inactivityKick.delayDays || 30,
        trackActivity: inactivityKick.trackActivity || false,
        excludedRoleIds: inactivityKick.excludedRoleIds || []
      },
      stats,
      members: members.slice(0, 100) // Limit to top 100
    });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// Get inactivity tracked members list
app.get('/api/inactivity/members', async (req, res) => {
  try {
    const guildId = req.query.guildId || DEFAULT_GUILD_ID;
    const config = await readBotConfig();
    
    if (!config.guilds || !config.guilds[guildId]) {
      return res.json([]);
    }
    
    const autokick = config.guilds[guildId].autokick || {};
    const inactivityKick = autokick.inactivityKick || { enabled: false };
    const tracking = autokick.inactivityTracking || {};
    
    const now = Date.now();
    const delayMs = (inactivityKick.delayDays || 30) * 24 * 60 * 60 * 1000;
    
    const members = [];
    
    for (const [userId, data] of Object.entries(tracking)) {
      const lastActivity = data.lastActivity || 0;
      const inactiveDuration = now - lastActivity;
      const daysInactive = Math.floor(inactiveDuration / (24 * 60 * 60 * 1000));
      const isInactive = inactiveDuration > delayMs;
      const hasWarning = data.graceWarningUntil && data.graceWarningUntil > now;
      const isPlanned = data.plannedInactive && data.plannedInactive.until > now;
      
      members.push({
        userId,
        lastActivity,
        daysInactive,
        isInactive,
        hasWarning,
        isPlanned,
        plannedReason: isPlanned ? data.plannedInactive.reason : null,
        plannedUntil: isPlanned ? data.plannedInactive.until : null
      });
    }
    
    // Sort by last activity (most recent first)
    members.sort((a, b) => b.lastActivity - a.lastActivity);
    
    res.json(members);
  } catch (err) {
    console.error('[API] Error getting inactivity members:', err);
    res.status(500).json({ error: err.message });
  }
});

// POST Reset member inactivity
app.post('/api/inactivity/reset-member', async (req, res) => {
  try {
    const { userId } = req.body;
    if (!userId) {
      return res.status(400).json({ error: 'userId is required' });
    }
    
    const config = await readBotConfig();
    const guildId = req.query.guildId || DEFAULT_GUILD_ID;
    
    if (!config.guilds || !config.guilds[guildId]) {
      return res.status(404).json({ error: 'Guild not found' });
    }
    
    const autokick = config.guilds[guildId].autokick || {};
    const tracking = autokick.inactivityTracking || {};
    
    if (!tracking[userId]) {
      return res.status(404).json({ error: 'Member not found in tracking' });
    }
    
    // Reset la lastActivity à maintenant
    tracking[userId].lastActivity = Date.now();
    
    // Supprimer les warnings et planned inactivity si présents
    if (tracking[userId].graceWarningUntil) {
      delete tracking[userId].graceWarningUntil;
    }
    
    config.guilds[guildId].autokick.inactivityTracking = tracking;
    
    await writeBotConfig(config);
    
    console.log(`[API] Reset inactivity for user ${userId}`);
    res.json({ success: true, message: 'Inactivity reset successfully' });
  } catch (e) {
    console.error('[API] Error resetting member inactivity:', e);
    res.status(500).json({ error: e.message });
  }
});

// GET Inactivity configuration
app.get('/api/inactivity', async (req, res) => {
  try {
    const guildId = req.query.guildId || DEFAULT_GUILD_ID;
    const config = await readBotConfig();
    
    if (!config.guilds || !config.guilds[guildId]) {
      return res.json({
        enabled: false,
        delayDays: 30,
        inactiveRoleId: null,
        excludedRoleIds: [],
        trackActivity: false
      });
    }
    
    const autokick = config.guilds[guildId].autokick || {};
    const inactivityKick = autokick.inactivityKick || {};
    
    res.json({
      enabled: inactivityKick.enabled || false,
      delayDays: inactivityKick.delayDays || 30,
      inactiveRoleId: inactivityKick.inactiveRoleId || null,
      excludedRoleIds: inactivityKick.excludedRoleIds || [],
      trackActivity: inactivityKick.trackActivity || false,
      gracePeriodDays: inactivityKick.gracePeriodDays || 7
    });
  } catch (e) {
    console.error('[API] Error getting inactivity config:', e);
    res.status(500).json({ error: e.message });
  }
});

// POST Save inactivity configuration
app.post('/api/inactivity', async (req, res) => {
  try {
    const guildId = req.query.guildId || DEFAULT_GUILD_ID;
    const config = await readBotConfig();
    
    if (!config.guilds) {
      config.guilds = {};
    }
    
    if (!config.guilds[guildId]) {
      config.guilds[guildId] = { autokick: {} };
    }
    
    if (!config.guilds[guildId].autokick) {
      config.guilds[guildId].autokick = {};
    }
    
    // Update inactivity kick config
    config.guilds[guildId].autokick.inactivityKick = {
      enabled: req.body.enabled || false,
      delayDays: req.body.delayDays || 30,
      inactiveRoleId: req.body.inactiveRoleId || null,
      excludedRoleIds: req.body.excludedRoleIds || [],
      trackActivity: req.body.trackActivity !== false, // true by default
      gracePeriodDays: req.body.gracePeriodDays || 7
    };
    
    await writeBotConfig(config);
    
    console.log(`[API] Inactivity config saved for guild ${guildId}`);
    res.json({ success: true, message: 'Configuration saved successfully' });
  } catch (e) {
    console.error('[API] Error saving inactivity config:', e);
    res.status(500).json({ error: e.message });
  }
});


// ============================================
// API ENDPOINTS: BOT CONTROL
// ============================================

// Get bot status and logs
app.get('/api/bot/status', async (req, res) => {
  try {
    const pm2List = await executeSSH('pm2 jlist');
    const data = JSON.parse(pm2List || '[]');
    const bagbot = data.find(p => p.name === 'bagbot');
    
    if (!bagbot) {
      return res.json({ online: false, message: 'Bot non trouvé' });
    }
    
    res.json({
      online: bagbot.pm2_env.status === 'online',
      status: bagbot.pm2_env.status,
      uptime: bagbot.pm2_env.pm_uptime,
      memory: bagbot.monit.memory,
      cpu: bagbot.monit.cpu,
      restarts: bagbot.pm2_env.restart_time,
      version: bagbot.pm2_env.version
    });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// Get bot logs
app.get('/api/bot/logs', async (req, res) => {
  try {
    const lines = parseInt(req.query.lines) || 100;
    const type = req.query.type || 'all'; // 'out', 'error', 'all'
    
    let command = '';
    if (type === 'out') {
      command = `tail -n ${lines} ~/.pm2/logs/bagbot-out.log`;
    } else if (type === 'error') {
      command = `tail -n ${lines} ~/.pm2/logs/bagbot-error.log`;
    } else {
      command = `pm2 logs bagbot --lines ${lines} --nostream`;
    }
    
    const logs = await executeSSH(command);
    res.json({ logs: logs || 'Aucun log disponible' });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// Restart bot
app.post('/api/bot/restart', async (req, res) => {
  try {
    await executeSSH('pm2 restart bagbot');
    res.json({ success: true, message: 'Bot redémarré avec succès' });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// Stop bot
app.post('/api/bot/stop', async (req, res) => {
  try {
    await executeSSH('pm2 stop bagbot');
    res.json({ success: true, message: 'Bot arrêté avec succès' });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// Start bot
app.post('/api/bot/start', async (req, res) => {
  try {
    await executeSSH('pm2 start bagbot');
    res.json({ success: true, message: 'Bot démarré avec succès' });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// Reload bot (zero-downtime)
app.post('/api/bot/reload', async (req, res) => {
  try {
    await executeSSH('pm2 reload bagbot');
    res.json({ success: true, message: 'Bot rechargé avec succès' });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// Clear bot cache
app.post('/api/bot/clear-cache', async (req, res) => {
  try {
    // Clear PM2 logs
    await executeSSH('pm2 flush bagbot');
    
    // Clear temp files if needed
    await executeSSH(`find ${BOT_BASE}/temp -type f -mtime +7 -delete 2>/dev/null || true`);
    
    res.json({ success: true, message: 'Cache vidé avec succès' });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// Get system info
app.get('/api/system/info', async (req, res) => {
  try {
    const [memory, cpu, disk, pm2List] = await Promise.all([
      executeSSH('free -m | grep Mem'),
      executeSSH('uptime'),
      executeSSH('df -h / | tail -1'),
      executeSSH('pm2 jlist')
    ]);
    
    // Parse memory
    const memParts = memory.trim().split(/\s+/);
    const memTotal = parseInt(memParts[1]);
    const memUsed = parseInt(memParts[2]);
    const memFree = parseInt(memParts[3]);
    
    // Parse disk
    const diskParts = disk.trim().split(/\s+/);
    const diskUsed = diskParts[4];
    
    // Count PM2 processes
    const processes = JSON.parse(pm2List || '[]');
    
    res.json({
      memory: {
        total: memTotal,
        used: memUsed,
        free: memFree,
        percent: Math.round((memUsed / memTotal) * 100)
      },
      disk: {
        used: diskUsed
      },
      uptime: cpu.trim(),
      processes: processes.length
    });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});


// Servir fichiers statiques (après toutes les routes API)
app.use(express.static(__dirname));

app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 BAG Bot Ultra Complete Dashboard API on port ${PORT}`);
  console.log(`🌐 http://82.67.65.98:${PORT}`);
});


// GET ECONOMY ACTIONS
app.get('/api/config/economy/actions', async (req, res) => {
  try {
    const guildId = req.query.guildId || DEFAULT_GUILD_ID;
    const config = await readBotConfig();
    const actions = config.guilds?.[guildId]?.economy?.actions?.config || {};
    res.json({ actions });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// UPDATE ECONOMY ACTION
app.post('/api/config/economy/actions/:actionName', async (req, res) => {
  try {
    const guildId = req.query.guildId || DEFAULT_GUILD_ID;
    const { actionName } = req.params;
    const updates = req.body;
    const config = await readBotConfig();
    if (!config.guilds) config.guilds = {};
    if (!config.guilds[guildId]) config.guilds[guildId] = {};
    if (!config.guilds[guildId].economy) config.guilds[guildId].economy = {};
    if (!config.guilds[guildId].economy.actions) config.guilds[guildId].economy.actions = {};
    if (!config.guilds[guildId].economy.actions.config) config.guilds[guildId].economy.actions.config = {};
    
    config.guilds[guildId].economy.actions.config[actionName] = updates;
    await writeBotConfig(config);
    res.json({ success: true });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// GET TRUTHDARE PROMPTS
app.get('/api/config/truthdare/prompts', async (req, res) => {
  try {
    const guildId = req.query.guildId || DEFAULT_GUILD_ID;
    const config = await readBotConfig();
    const td = config.guilds?.[guildId]?.truthdare || {};
    
    // Les prompts sont dans sfw.prompts et nsfw.prompts
    const sfwPrompts = td.sfw?.prompts || [];
    const nsfwPrompts = td.nsfw?.prompts || [];
    
    // Séparer par type (action vs verite)
    const sfwActions = sfwPrompts.filter(p => p.type === 'action');
    const sfwTruths = sfwPrompts.filter(p => p.type === 'verite');
    const nsfwActions = nsfwPrompts.filter(p => p.type === 'action');
    const nsfwTruths = nsfwPrompts.filter(p => p.type === 'verite');
    
    res.json({ 
      customActions: { 
        sfw: sfwActions, 
        nsfw: nsfwActions 
      },
      customTruths: { 
        sfw: sfwTruths, 
        nsfw: nsfwTruths 
      }
    });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// ADD TRUTHDARE PROMPT
app.post('/api/config/truthdare/prompts', async (req, res) => {
  try {
    const guildId = req.query.guildId || DEFAULT_GUILD_ID;
    const { type, mode, text } = req.body; // type: action|truth, mode: sfw|nsfw
    const config = await readBotConfig();
    if (!config.guilds) config.guilds = {};
    if (!config.guilds[guildId]) config.guilds[guildId] = {};
    if (!config.guilds[guildId].truthdare) config.guilds[guildId].truthdare = {};
    
    const key = type === 'action' ? 'customActions' : 'customTruths';
    if (!config.guilds[guildId].truthdare[key]) config.guilds[guildId].truthdare[key] = { sfw: [], nsfw: [] };
    if (!config.guilds[guildId].truthdare[key][mode]) config.guilds[guildId].truthdare[key][mode] = [];
    
    config.guilds[guildId].truthdare[key][mode].push(text);
    await writeBotConfig(config);
    res.json({ success: true });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// DELETE TRUTHDARE PROMPT
app.delete('/api/config/truthdare/prompts', async (req, res) => {
  try {
    const guildId = req.query.guildId || DEFAULT_GUILD_ID;
    const { type, mode, index } = req.body;
    const config = await readBotConfig();
    const key = type === 'action' ? 'customActions' : 'customTruths';
    
    if (config.guilds?.[guildId]?.truthdare?.[key]?.[mode]) {
      config.guilds[guildId].truthdare[key][mode].splice(index, 1);
      await writeBotConfig(config);
    }
    res.json({ success: true });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// GET TICKETS CONFIG
app.get('/api/config/tickets', async (req, res) => {
  try {
    const guildId = req.query.guildId || DEFAULT_GUILD_ID;
    const config = await readBotConfig();
    const tickets = config.guilds?.[guildId]?.tickets || {};
    res.json({ tickets });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// GET ECONOMY ACTIONS from bot.js
app.get('/api/config/economy/actions-from-bot', async (req, res) => {
  try {
    const guildId = req.query.guildId || DEFAULT_GUILD_ID;
    const config = await readBotConfig();
    const actions = config.guilds?.[guildId]?.economy?.actions?.config || {};
    res.json({ actions, count: Object.keys(actions).length });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.post('/api/config/tickets', async (req, res) => {
  try {
    const guildId = req.query.guildId || DEFAULT_GUILD_ID;
    const config = await readBotConfig();
    
    if (!config.guilds[guildId].tickets) {
      config.guilds[guildId].tickets = {};
    }
    
    // Merge updates
    Object.assign(config.guilds[guildId].tickets, req.body);
    
    await writeBotConfig(config);
    res.json({ success: true });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// RENAME COMMANDS
app.post('/api/commands/rename', async (req, res) => {
  try {
    const { commands } = req.body;
    // TODO: Implémenter la logique de renommage des commandes
    // Pour l'instant on simule le succès
    res.json({ success: true, renamed: commands.length });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});
