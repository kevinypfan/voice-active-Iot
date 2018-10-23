import '@babel/polyfill'
import Vue from 'vue'
import VueMqtt from 'vue-mqtt';
import './plugins/axios'
import './plugins/vuetify'
import App from './App.vue'

Vue.use(VueMqtt, 'mqtt broker');
Vue.config.productionTip = false

new Vue({
  render: h => h(App)
}).$mount('#app')
