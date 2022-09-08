<template>
    <div class="container">
      <siteHeader/>
      <siteMenu/>
      <siteMain/>
      <siteFooter/>
    </div>
</template>

<script>
import siteHeader from './components/header/site-header.vue'
import siteMenu from './components/menu/site-menu.vue'
import siteMain from './components/main/site-main.vue'
import siteFooter from './components/footer/site-footer.vue'

export default {
  name: 'App',
  components: {
    siteHeader,
    siteMenu,
    siteMain,
    siteFooter
  }
}
</script>

<style lang='scss'>
.container{
  min-width: 600px;
}
</style>
