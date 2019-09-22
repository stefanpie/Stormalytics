import Vue from 'vue'
import App from './App.vue'

const AppData = {msg: 'hello'}


new Vue({
  el: '#app',
  render: h => h(App),
  data: AppData
})
