import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import SummonerInfo from '@/components/SummonerInfo'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/:server/:summonerName',
      name: 'summonerInfo',
      component: SummonerInfo,
      props: true,
    }
  ]
})
