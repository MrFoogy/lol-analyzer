import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import router from './router'
import 'es6-promise/auto'

Vue.config.productionTip = false
Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    accountId: "",
    summonerId: "",
  },
  mutations: {
    setAccountId(state, newId) {
      state.accountId = newId;
    },
    setSummonerId(state, newId) {
      state.summonerId = newId;
    }
  }
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
