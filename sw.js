// v5：透明网络穿透版 Service Worker。
// 设计目标：彻底消除「升级后仍显示旧版 / 作者名不出现」这类缓存陷阱。
//  - 不再缓存 index.html / quotes.json 等任何资源（全部走网络），保证内容永远最新。
//  - 激活后立即 claim 所有页面，并强制刷新每一个已打开的页面，
//    把手机端可能滞留的旧 HTML 一次性甩掉。
//  - 仍保留 SW 以支持「添加到主屏幕」，但不再承担缓存职责。

const APP_VERSION = '5';

self.addEventListener('install', (event) => {
  // 安装即跳过等待，尽快接管
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      // 1) 清空一切历史缓存（v1~v4 留下的旧内容）
      const keys = await caches.keys();
      await Promise.all(keys.map((k) => caches.delete(k)));
      // 2) 立即接管所有页面（含未被 SW 控制的）
      await self.clients.claim();
      // 3) 强制刷新所有已打开的页面，甩开旧 HTML
      const clients = await self.clients.matchAll({ includeUncontrolled: true });
      clients.forEach((c) => {
        try { c.navigate(c.url); } catch (e) { /* 忽略个别客户端导航失败 */ }
      });
    })()
  );
});

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'skipWaiting') self.skipWaiting();
});

self.addEventListener('fetch', (event) => {
  // 完全穿透：直接请求网络，不做任何缓存。
  event.respondWith(fetch(event.request));
});
