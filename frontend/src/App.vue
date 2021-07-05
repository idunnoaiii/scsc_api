<template>
  <v-app id="app-body">
    <div>
      <v-app-bar color="deep-purple">
        <v-toolbar-title class="white--text">SCSC Bakery </v-toolbar-title>
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
            to="/inventory"
          >
            <v-icon left dark> mdi-store </v-icon>Inventory
          </v-btn>

          <v-btn
            small
            color="deep-purple  "
            class="white--text"
            @click="showDialog('Login')"
          >
            <v-icon left dark> mdi-basket </v-icon> Category
          </v-btn>

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

          <v-btn
            small
            color="deep-purple  "
            class="white--text"
            @click="showDialog('Transcation')"
          >
            <v-icon left dark> mdi-card-account-details-outline </v-icon>
            Transaction
          </v-btn>

          <v-btn small color="deep-purple  " class="white--text" to="/users">
            <v-icon left dark> mdi-account </v-icon> User
          </v-btn>
          <v-btn small color="deep-purple  " class="white--text">
            <v-icon left dark> mdi-account </v-icon> Admin
          </v-btn>

          <v-btn small color="green" dark @click="showScanDialog">
            <v-icon centered dark> mdi-cog-outline </v-icon>
          </v-btn>

          <v-btn small dark color="red">
            <v-icon centered dark> mdi-logout-variant </v-icon>
          </v-btn>
        </v-toolbar-items>
      </v-app-bar>
    </div>
    <!-- Sizes your content based upon application components -->
    <v-main>
      <!-- Provides the application the proper gutter -->
      <!-- If using vue-router -->
      <v-container fluid fill-height>
        <keep-alive>
          <transition name="fade">
            <router-view> </router-view>
          </transition>
        </keep-alive>
      </v-container>
    </v-main>
    <Dialog v-if="$store.state.dialogViewName">
      <template v-slot:dialogBody>
        <!-- <keep-alive> -->
          <component :is="$store.state.dialogViewName"></component>
        <!-- </keep-alive> -->
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

.fade-enter-active, .fade-leave-active {
  transition: opacity .3s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
