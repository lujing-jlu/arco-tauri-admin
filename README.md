![21c116e2bfaca64f9934e3094f673970](https://github.com/lujing-jlu/arco-tauri-admin/assets/20335721/7b82d20a-5ed5-48f0-bcb4-62ce57586dae)

```shell
npm i -g arco-cli
npm i -g pnpm

arco init arco-tauri-admin

pnpm add -D @tauri-apps/cli

pnpm tauri init


# arco-tauri-admin\config\vite.config.dev.ts
# 添加vite server的ip和port，防止和wsl冲突
...
export default mergeConfig(
  {
    mode: 'development',
    server: {
      host: '127.0.0.1',
      port: 3000,
...


pnpm tauri dev


pnpm tauri build
```
