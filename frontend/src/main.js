import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import VueSweetalert2 from 'vue-sweetalert2'
import VMdDateRangePicker from "v-md-date-range-picker";
import VueHtmlToPaper from 'vue-html-to-paper';


import 'sweetalert2/dist/sweetalert2.min.css';
// import "v-md-date-range-picker/dist/v-md-date-range-picker.css";

Vue.use(VMdDateRangePicker);

Vue.config.productionTip = false

Vue.use(VueSweetalert2, {
  confirmButtonColor: '#41b882',
  cancelButtonColor: '#ff7674',
})

Vue.use(VueHtmlToPaper);

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')


// router.replace('/login')