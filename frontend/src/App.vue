<template>
  <v-app id="app-body">
    <div>
      <v-app-bar v-if="$store.state.isAuthenticated" color="primary" app>
        <v-toolbar-title class="white--text" link to="/"
          >SCSC Bakery</v-toolbar-title
        >
        <v-spacer></v-spacer>
        <v-toolbar-items>
          <v-btn
            small
            width="80px"
            :color="`primary ${
              $store.state.scanMode == true ? 'lighten-2' : ''
            }`"
            dark
            @click="toggleScanningMode"
          >
            <v-icon centered dark> mdi-camera </v-icon>
          </v-btn>
          <v-btn small color="primary  " class="white--text" to="/test">
            <v-icon left dark> mdi-card-account-details-outline </v-icon>
            test
          </v-btn>
          <v-btn small color="primary " class="white--text" to="/">
            <v-icon left dark> mdi-card-account-details-outline </v-icon> Point
            of Sale
          </v-btn>
          <v-btn small color="primary  " class="white--text" to="/transaction">
            <v-icon left dark> mdi-card-account-details-outline </v-icon>
            Transaction
          </v-btn>
          <v-menu offset-y rounded="0">
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
                <v-list-item-title class="white--text"
                  >Account</v-list-item-title
                >
              </v-list-item>
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
                <v-icon left dark>mdi-account </v-icon>Admin
              </v-btn>
            </template>
            <v-list color="primary  " class="white--text">
              <v-list-item link to="/inventory">
                <v-list-item-title class="white--text"
                  >Profile</v-list-item-title
                >
              </v-list-item>
              <v-list-item link @click="logout">
                <v-list-item-title class="white--text"
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
      <v-navigation-drawer v-model="$store.state.itemDialog" width="33%" absolute temporary>
        <ItemBoard/>
      </v-navigation-drawer>
    </div>
    <!-- Sizes your content based upon application components -->
    <v-main>
      <!-- Provides the application the proper gutter -->
      <!-- If using vue-router -->
      <v-container fluid fill-height>
        <keep-alive>
          <router-view> </router-view>
        </keep-alive>
      </v-container>
    </v-main>
    <Dialog v-if="$store.state.dialog">
      <template v-slot:dialogBody>
        <component :is="$store.state.dialogViewName"></component>
      </template>
    </Dialog>

    <ScanDialog v-if="$store.state.scanDialog"></ScanDialog>
  </v-app>
</template>


<script>
import Dialog from "./components/Dialog.vue";
import ScanDialog from "./components/ScanDialog.vue";
import ItemBoard from "./components/ItemBoard.vue";
import User from "./views/pages/User.vue";
import POS from "./views/pages/POS.vue";
import Login from "./views/pages/Login.vue";
import * as muType from "./store/mutation-type";
import axios from "./axios";
import AddCustomer from "./components/AddCustomer.vue";

export default {
  name: "App",
  components: {
    Dialog,
    ScanDialog,
    User,
    POS,
    Login,
    AddCustomer,
    ItemBoard
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
      localStorage.removeItem("token");
      this.$store.commit("SET_LOGIN_TOKEN", "");
      this.$store.commit("SET_AUTH_STATUS", false);
      this.$router.replace("/login");
    },
    toggleScanningMode() {
      this.$store.commit("TOGGLE_SCAN_MODE");
    },
  },
  beforeCreate: function () {
    this.$store.commit("INITIALIZE_STORE");
    axios.defaults.headers.common["Authorization"] = this.$store.state.token;
  },
};
</script>


<style lang="scss" scoped>
body {
  background: linear-gradient(40deg, #77008cde, #041158ec);
  font-family: "Roboto", sans-serif;
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
