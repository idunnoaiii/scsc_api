import Vue from 'vue'
import Vuex from 'vuex'
import * as muType from './mutation-type'
import POS from './modules/POS'
import { parseJwt } from '../utils'

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
    isAdmin: false,
    username: null,
    userid: 0,
    scanMode: true,
    itemDialog: false,
    addCustomerDialog: false,
    capturedResponse: { items: [], positions: [] },
    capturedItemPicked: null,
    capturedItemPickedIndex: null,
    isDrawing: false,
    userProfile: false,
    changePassword: false,
    toast: false,
    toastMsg: "",
    toastColor: "",
    positions_updated: false,
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
    SET_USERNAME(state, username) {
      state.username = username
    }, SET_USERID(state, userid) {
      state.userid = userid
    },
    SET_PAYDIALOG(state, status) {
      state.payDialog = status
    },
    SET_ITEM_DIALOG(state, status) {
      state.itemDialog = status
    },
    INITIALIZE_STORE(state) {
      const token = localStorage.getItem("token")
      state.token = token != null ? token : "";
      state.isAuthenticated = token != null ? true : false;
      let jwtObj = parseJwt(token);
      let sub = JSON.parse(jwtObj.sub)
      state.isAdmin = sub.is_admin;
      state.username = sub.username;
      state.userid = sub.id;
    },
    TOGGLE_SCAN_MODE(state) {
      state.scanMode = !state.scanMode;
    },
    SET_SCAN_MODE(state, status) {
      state.scanMode = status
    },
    SET_CAPTURED_RESPONSE(state, data) {
      state.capturedResponse = data
    },

    SET_ADD_CUSTOMER(state, status){
      if(status !== null){
        state.addCustomerDialog = status;
        return;
      }
      state.addCustomerDialog = !state.addCustomerDialog;
    },

    REMOVE_CAPTURED_ITEM(state, index) {
      console.log("REMOVE_CAPTURED_ITEM")
      if (state.capturedResponse && state.capturedResponse.positions) {
        state.capturedResponse.positions[index] = null
        console.log(state.capturedResponse.positions)
        state.positions_updated = true;
      }
    },
    SET_CAPTURED_ITEM_PICK(state, payload) {
      if (state.capturedResponse.items !== null) {
        state.capturedItemPicked = state.capturedResponse.items.find(x => x.id == payload.id)
      }
      state.capturedItemPickedIndex = payload.index
      if (state.capturedItemPicked == null) {
        state.capturedResponse.positions.push([-1, ...payload.positions, 0])
        state.capturedItemPickedIndex = state.capturedResponse.positions.length - 1
        state.positions_updated = true;
      }
      state.updateBox = payload.update
      console.log(state.updateBox)
    },
    CHANGE_CAPTURED_ITEM_PICK(state, item) {
      console.log(state.capturedResponse.positions[state.capturedItemPickedIndex][0], item.id)
      state.capturedResponse.positions[state.capturedItemPickedIndex][0] = item.id
      if (state.capturedResponse.items == null || state.capturedResponse.items.find(x => x.id == item.id) == null)
        state.capturedResponse.items.push(item)
      state.updateBox(item.name, item.price, state.capturedItemPickedIndex, item.id)
      state.capturedItemPicked = null
      state.positions_updated = true;
      console.log(state.capturedResponse.positions)
    },
    SET_DRAWING(state, status) {
      if (status != null) {
        state.isDrawing = status;
        return
      }
      state.isDrawing = !state.isDrawing
    },
    SET_USER_PROFILE(state, status) {
      if (status != null) {
        state.userProfile = status;
      }
      state.userProfile = !state.userProfile
    },
    SET_CHANGE_PASSWORD(state, status) {
      if (status != null) {
        state.changePassword = status;
        console.log(state.changePassword)
        return
      }
      state.changePassword = !state.changePassword
    },
    SET_TOAST(state, payload) {
      state.toast = true
      state.toastMsg = payload.toastMsg
      state.toastColor = payload.toastColor
      console.log(state.toast, "TOAS")
    },
    RESET_POSITION_UPDATED_FLAG(state){
      state.positions_updated = false;
    }

  },
  actions: {

  },
  modules: {
    POS
  }
})


