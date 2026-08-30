# Photo · 图片工坊

`photo.tinylabpro.com` 的独立前端项目，第一版包含两个工具：

- **证件照制作**：浏览器本地人像抠图、红白蓝底、常用规格、位置微调、基础质量提示、电子照和六寸排版照。
- **图片与 Logo 处理**：裁剪式缩放、位置调整、旋转、智能去背景、边角颜色转透明、尺寸修改、PNG/JPG/WebP 转换与压缩。

## 隐私与限制

- 图片只在浏览器中处理，不上传到服务器。
- 支持 PNG、JPG、WebP；单张最大 10 MB、2400 万像素。
- 不接受 SVG 和 GIF。
- Canvas 重新编码导出，不保留 EXIF、GPS 等元数据。
- 第一次智能去背景会下载约 40 MB 的量化模型，之后由浏览器缓存。
- 证件照预设只作常见参考，用户仍需核对办理机构的最新要求。

## 本地运行

需要 Node.js 24 或更新版本：

```bash
npm install
npm run dev
```

生产构建：

```bash
npm run build
npm run preview
```

## Docker

```bash
docker compose up -d --build
```

容器内部监听 `8080`，暂时不映射宿主机端口。添加域名时，让 Cloudflare Tunnel 的
`photo.tinylabpro.com` 指向 `http://photo:8080`，并把 photo 服务接入 Tunnel 所在的 Docker 网络。

## 背景移除组件

项目使用 `@imgly/background-removal` 在浏览器本地做人像分割。该组件采用 AGPL 许可；
正式发布时应公开本项目对应版本的源代码，并保留第三方许可说明。

当前模型默认从 IMG.LY 的静态资源地址下载。正式部署前建议将对应模型资源放到自己的
`photo.tinylabpro.com`，避免依赖外部 CDN。

## 后续衔接 unmark

当前两个工具完全独立。后续增加一次性交接令牌后，可以从 unmark 的处理结果进入图片工坊，
处理 Logo 后再回到 unmark 完成文档叠加；不要在跨域链接里直接暴露文档任务编号。

