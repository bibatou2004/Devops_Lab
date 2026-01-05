module.exports = {
  apps: [{
    name: "sample-app",
    script: "./app.js",
    exec_mode: "cluster",
    instances: "max",
    env: {
      "NODE_ENV": "production",
      "APP_VERSION": "1.0"
    },
    error_file: "/home/app-user/logs/err.log",
    out_file: "/home/app-user/logs/out.log",
    log_date_format: "YYYY-MM-DD HH:mm:ss Z"
  }]
}
