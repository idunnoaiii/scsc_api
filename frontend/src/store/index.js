import Vue from 'vue'
import Vuex from 'vuex'
import * as muType from './mutation-type'
import POS from './modules/POS'

Vue.use(Vuex)

// export default new Vuex.Store({
//   modules:{
//     POS
//   }
// })

export default new Vuex.Store({
  state: {
    dialog: false,
    scanDialog: false,
    dialogViewName: 'User',
    isAuthenticated: false,
    payDialog: false,
    token: '',
    isAdmin: false
  },
  mutations: {
    [muType.SHOW_GLOBAL_DIALOG](state, name) {
      state.dialog = !state.dialog
      state.dialogViewName = name
    },
    [muType.TOGGLE_SCAN_DIALOG](state) {
      state.scanDialog = !state.scanDialog
    },
    SET_LOGIN_TOKEN(state, token) {
      state.token = token
    },
    SET_AUTH_STATUS(state, status) {
      state.isAuthenticated = status
    },
    SET_ROLE(state, status) {
      state.isAdmin = status
    },
    SET_PAYDIALOG(state, status) {
      state.payDialog = status
    },
    INITIALIZE_STORE(state) {
      const token = localStorage.getItem("token")
      state.token = token != null ? token : "";
      state.isAuthenticated = token != null ? true : false;
    }
  },
  actions: {

  },
  modules: {
    POS
  }
})


