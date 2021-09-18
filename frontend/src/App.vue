<template>
  <v-app id="app-body">
    <div id="vue-nav-bar">
      <v-app-bar v-if="$store.state.isAuthenticated" color="primary" app>
        <v-toolbar-title class="white--text" link to="/">SCSC</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items>
          <!-- <v-btn
            small
            width="80px"
            color="primary"
            dark
            @click="
              $store.commit('SET_TOAST', {
                toastMsg: 'ahihi',
                toastColor: 'orange',
              })
            "
          >
            TEST </v-btn> -->
          <v-btn
            small
            width="80px"
            :color="`primary ${
              $store.state.scanMode == true ? 'lighten-2' : ''
            }`"
            dark
            @click="toggleScanningMode"
            v-if="!$store.state.isAdmin"
          >
            <v-icon left dark> mdi-camera </v-icon>
            Scan
          </v-btn>
          <!-- <v-btn small color="primary  " class="white--text" to="/test">
            <v-icon left dark> mdi-card-account-details-outline </v-icon>
            test
          </v-btn> -->
          <!-- <v-btn
            small
            color="primary "
            class="white--text"
            to="/pos"
            v-if="!$store.state.isAdmin"
          >
            <v-icon left dark> mdi-card-account-details-outline </v-icon>
            Checkout
          </v-btn> -->
          <v-btn
            small
            color="primary  "
            class="white--text"
            to="/transaction"
            v-if="$store.state.isAdmin"
          >
            <v-icon left dark> mdi-card-account-details-outline </v-icon>
            Sales report
          </v-btn>
          <v-menu offset-y rounded="0" v-if="$store.state.isAdmin">
            <template v-slot:activator="{ on, attrs }">
              <v-btn small color="primary  " dark v-bind="attrs" v-on="on">
                <v-icon left dark> mdi-store </v-icon>Manage Store
              </v-btn>
            </template>
            <v-list color="primary  " class="white--text">
              <v-list-item link to="/inventory">
                <v-list-item-title class="white--text">Item</v-list-item-title>
              </v-list-item>
              <v-list-item link to="/category">
                <v-list-item-title class="white--text"
                  >Category</v-list-item-title
                >
              </v-list-item>
              <v-list-item link to="/discount">
                <v-list-item-title class="white--text"
                  >Discount</v-list-item-title
                >
              </v-list-item>
              <v-list-item link to="/users">
                <v-list-item-title class="white--text">User</v-list-item-title>
              </v-list-item>
              <!-- <v-list-item link to="/customer">
                <v-list-item-title class="white--text"
                  >Customer</v-list-item-title
                >
              </v-list-item> -->
            </v-list>
          </v-menu>

          <!-- <div class="d-inline-block elevation-2 ">
                <v-btn elevation="0" small class="rounded-0" color="white ">
                  <v-icon left dark> mdi-store </v-icon>Sản phẩm
                </v-btn>
                <v-btn elevation="0" small class="rounded-0" color="primary">
                  <v-icon left dark class="mx-0"> mdi-plus </v-icon>
                </v-btn>
              </div>
              <div class="d-inline-block elevation-2">
                <v-btn elevation="0" small class="rounded-0" color="white ">
                  <v-icon left dark> mdi-store </v-icon>Sản phẩm
                </v-btn>
                <v-btn elevation="0" small class="rounded-0" color="primary">
                  <v-icon left dark class="mx-0"> mdi-plus </v-icon>
                </v-btn>
              </div> -->
          <!-- <v-btn elevation="0" medium dark color="red">
              <v-icon centered dark class="mx-0"> mdi-power </v-icon>
            </v-btn> -->

          <!-- <v-btn small color="primary  " class="white--text">
            <v-icon left dark> mdi-account </v-icon> Admin
          </v-btn> -->

          <v-menu offset-y rounded="0">
            <template v-slot:activator="{ on, attrs }">
              <v-btn small color="primary  " dark v-bind="attrs" v-on="on">
                <v-icon left dark>mdi-account </v-icon
                >{{ $store.state.username }}
              </v-btn>
            </template>
            <v-list color="primary  " class="white--text">
              <v-list-item
                link
                @click="$store.commit('SET_USER_PROFILE', null)"
              >
                <v-list-item-title class="white--text"
                  >Profile</v-list-item-title
                >
              </v-list-item>
              <v-list-item
                link
                @click="$store.commit('SET_CHANGE_PASSWORD', null)"
              >
                <v-list-item-title class="white--text" @click="logout"
                  >Logout</v-list-item-title
                >
              </v-list-item>
            </v-list>
          </v-menu>

          <!-- <v-btn small dark color="red">
            <v-icon centered dark> mdi-logout-variant </v-icon>
          </v-btn> -->
        </v-toolbar-items>
      </v-app-bar>
      <v-navigation-drawer
        v-model="$store.state.itemDialog"
        width="33%"
        absolute
        temporary
      >
        <ItemBoard />
      </v-navigation-drawer>
    </div>
    <!-- Sizes your content based upon application components -->
    <v-main>
      <!-- Provides the application the proper gutter -->
      <!-- If using vue-router -->
      <v-container fluid fill-height>
        <!-- <keep-alive> -->
        <router-view> </router-view>
        <!-- </keep-alive> -->
      </v-container>
    </v-main>
    <Dialog v-if="$store.state.dialog">
      <template v-slot:dialogBody>
        <component :is="$store.state.dialogViewName"></component>
      </template>
    </Dialog>

    <ScanDialog v-if="$store.state.scanDialog"></ScanDialog>
    <UserProfile v-if="$store.state.userProfile"></UserProfile>
    <v-snackbar
      timeout="2000"
      v-model="$store.state.toast"
      :color="$store.state.toastColor"
      absolute
      top
      right
      app
      min-height="70"
      dark
      style="z-index: 999"
      prominent
      transition="slide-x-reverse-transition"
    >
      {{ $store.state.toastMsg }}
    </v-snackbar>
  </v-app>
</template>


<script>
import Dialog from "./components/Dialog.vue";
import ScanDialog from "./components/ScanDialog.vue";
import ItemBoard from "./components/ItemBoard.vue";
import UserProfile from "./components/UserProfile.vue";
import User from "./views/pages/User.vue";
import POS from "./views/pages/POS.vue";
import Login from "./views/pages/Login.vue";
import PrintInvoice from "./views/pages/PrintInvoice.vue";
import Checkout from "./views/pages/Checkout.vue"
import * as muType from "./store/mutation-type";
import axios from "./axios";
import { mapMutations } from "vuex";

export default {
  name: "App",
  components: {
    Dialog,
    ScanDialog,
    User,
    POS,
    Login,
    ItemBoard,
    UserProfile,
    PrintInvoice,
    Checkout
  },
  data: () => ({
    isLogined: true,
  }),
  methods: {
    showDialog: function (name) {
      this.$store.commit(muType.SHOW_GLOBAL_DIALOG, name);
    },
    showScanDialog: function () {
      this.$store.commit(muType.TOGGLE_SCAN_DIALOG);
    },
    initialize() {},
    logout() {
      console.log("logout");
      localStorage.removeItem("token");
      this.$store.commit("SET_LOGIN_TOKEN", "");
      this.$store.commit("SET_AUTH_STATUS", false);
      this.$router.push("/login");
    },
    toggleScanningMode() {
      this.$store.commit("TOGGLE_SCAN_MODE");
    },
    ...mapMutations("POS", {
      setOrderCode: "SET_ORDER_CODE",
    }),
  },
  beforeCreate: function () {
    const token = localStorage.getItem("token");
    if (token) {
      this.$store.commit("INITIALIZE_STORE");
      axios.defaults.headers.common["Authorization"] = this.$store.state.token;
    }
  },

  mounted() {
    this.setOrderCode();
  },
};
</script>


<style lang="scss" scoped>
body {
  background: linear-gradient(40deg, #77008cde, #041158ec);
  font-family: "Lato", sans-serif;
}

#app-body {
  max-height: 100vh;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.33s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
