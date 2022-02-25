module.exports = {
  apps : [{
    name: "Redis-commander",
    script: "/opt/tklweb-cp/node_modules/redis-commander/bin/redis-commander.js",
    args: "--address 127.0.0.1 --port 8082 --redis-user=default --redis-password='turnkey1'",
    env: {
      "NODE_ENV": "production",
      "HTTP_USER": "admin",
      "HTTP_PASSWORD": "turnkeypw"
    }
  }, {
    name: "TurnKey Linux CP",
    script: "/opt/tklweb-cp/tklweb-cp.js"
  }],

  deploy : {
  }
};
