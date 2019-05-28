import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home.vue'
import SummonerMain from '@/views/SummonerMain.vue'
import SummonerInfo from '@/views/SummonerInfo'
import SummonerChampions from '@/views/SummonerChampions'
import SummonerMatches from '@/views/SummonerMatches'

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
      name: 'summonerMain',
      component: SummonerMain,
      props: true,
      children: [
        {
          path: '',
          redirect: 'overview',
        },
        {
          path: 'overview',
          name: 'summonerOverview',
          props: true,
          component: SummonerInfo,
        },
        {
          path: 'champions',
          name: 'summonerChampions',
          props: true,
          component: SummonerChampions,
        },
        {
          path: 'matches',
          name: 'summonerMatches',
          props: true,
          component: SummonerMatches,
        }
      ]
    }
  ]
})
