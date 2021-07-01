import Vue from 'vue'
import Vuex from 'vuex'
// import * as muType from './mutation-type'
import POS from './modules/POS'

Vue.use(Vuex)

export default new Vuex.Store({
  modules:{
    POS
  }
})

// export default new Vuex.Store({
//   state: {
//     dialog: false,
//     scanDialog: false,
//     dialogViewName: ''
//   },
//   mutations: {
//     [muType.SHOW_GLOBAL_DIALOG](state, name){
//       state.dialog = !state.dialog
//       state.dialogViewName = name
//     },
//     [muType.TOGGLE_SCAN_DIALOG](state){
//       state.scanDialog = !state.scanDialog
//     }
//   },
//   actions: {
//   },
//   modules: {
//   }
// })


