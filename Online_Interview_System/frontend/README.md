# online-interview-system front-end

> The front-end of an online interview system based on Vue.js

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build
```

## 面试房间

在 `npm run dev` 之后会出现 `hello world` 页面，上面有到 interviewee 房间的链接。

每个部分作为一个组件，都在文件夹 `./src/intvweeviews/` 内
白板对应的文件为 `./src/intvweeviews/Board.vue`
代码编辑对应的文件为`./src/intvweeviews/Editor.vue`
文字聊天对应的文件为`./src/intvweeviews/Text.vue`
视频对应的文件为`./src/intvweeviews/Video.vue`

每个部分应该打包成一个自定义的标签，比如视频部分可以打包成 `<my-video></my-video>`

比如要加入视频部分的组件，假如视频部分的顶层文件名为 `Index.vue`，可以新建一个文件夹 `/src/intvweeviews/video` 将视频部分对应的 vue 文件全部放入该文件夹下（假如视频部分的顶层文件名为 `Index.vue`），然后在对应的文件 `./src/intvweeviews/Video.vue` 中 `import MyVideo from './intvweeviews/video/Index'`，然后在该文件的 `<template></template>` 内加入 `<my-video></my-video>`