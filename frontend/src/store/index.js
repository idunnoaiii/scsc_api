import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    dialog: false,
    dialogViewName: ''
  },
  mutations: {
    showDialog(state, name){
      state.dialog = !state.dialog
      state.dialogViewName = name
    }
  },
  actions: {
  },
  modules: {
  }
})
