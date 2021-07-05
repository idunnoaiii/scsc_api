<template>
  <v-app id="app-body">
    <div>
      <v-app-bar v-if="this.$store.state.isAuthenticated" color="deep-purple" app>
        <v-toolbar-title class="white--text" link to="/"
          >SCSC Bakery</v-toolbar-title
        >
        <v-spacer></v-spacer>
        <v-toolbar-items>
          <v-btn small color="deep-purple  " class="white--text" to="/test">
            <v-icon left dark> mdi-card-account-details-outline </v-icon>
            test
          </v-btn>
          <v-btn small color="deep-purple  " class="white--text" to="/">
            <v-icon left dark> mdi-card-account-details-outline </v-icon> Point
            of Sale
          </v-btn>
          <v-btn
            small
            color="deep-purple  "
            class="white--text"
            to="/transaction"
          >
            <v-icon left dark> mdi-card-account-details-outline </v-icon>
            Transaction
          </v-btn>
          <v-menu offset-y rounded="0">
            <template v-slot:activator="{ on, attrs }">
              <v-btn small color="deep-purple  " dark v-bind="attrs" v-on="on">
                <v-icon left dark> mdi-store </v-icon>Manage Store
              </v-btn>
            </template>
            <v-list color="deep-purple  " class="white--text">
              <v-list-item link to="/inventory">
                <v-list-item-title class="white--text">Item</v-list-item-title>
              </v-list-item>
              <v-list-item link to="/category">
                <v-list-item-title class="white--text"
                  >Category</v-list-item-title
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

          <!-- <v-btn small color="deep-purple  " class="white--text">
            <v-icon left dark> mdi-account </v-icon> Admin
          </v-btn> -->

           <v-menu offset-y rounded="0">
            <template v-slot:activator="{ on, attrs }">
              <v-btn small color="deep-purple  " dark v-bind="attrs" v-on="on">
                <v-icon left dark>mdi-account </v-icon>Admin
              </v-btn>
            </template>
            <v-list color="deep-purple  " class="white--text">
              <v-list-item link to="/inventory">
                <v-list-item-title class="white--text">Profile</v-list-item-title>
              </v-list-item>
              <v-list-item link to="/category">
                <v-list-item-title class="white--text"
                  >Logout</v-list-item-title
                >
              </v-list-item>
            </v-list>
          </v-menu>

          <!-- <v-btn small color="green" dark @click="showScanDialog">
            <v-icon centered dark> mdi-cog-outline </v-icon>
          </v-btn> -->

          <!-- <v-btn small dark color="red">
            <v-icon centered dark> mdi-logout-variant </v-icon>
          </v-btn> -->
        </v-toolbar-items>
      </v-app-bar>
    </div>
    <!-- Sizes your content based upon application components -->
    <v-main>
      <!-- Provides the application the proper gutter -->
      <!-- If using vue-router -->
      <v-container fluid fill-height>
        <transition name="fade">
          <keep-alive>
            <router-view> </router-view>
          </keep-alive>
        </transition>
      </v-container>
    </v-main>
    <Dialog v-if="$store.state.dialogViewName">
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
import User from "./views/pages/User.vue";
import POS from "./views/pages/POS.vue";
import * as muType from "./store/mutation-type";

export default {
  name: "App",
  components: {
    Dialog,
    ScanDialog,
    User,
    POS,
  },
  data: () => ({
    items: [
      { title: "Click Me" },
      { title: "Click Me" },
      { title: "Click Me" },
      { title: "Click Me 2" },
    ],
  }),
  methods: {
    showDialog: function (name) {
      this.$store.commit(muType.SHOW_GLOBAL_DIALOG, name);
    },
    showScanDialog: function () {
      this.$store.commit(muType.TOGGLE_SCAN_DIALOG);
    },
    initialize() {},
  },
  created() {
    this.initialize();
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
