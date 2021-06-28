<template>
  <v-app id="dashboard">
    <v-container fluid>
      <v-row no-gutters class="mt-2">
        <v-col class="d-flex flex-row justify-start col-md-4">
          <div class="d-inline-block elevation-2">
            <v-btn
              elevation="0"
              small
              tile
              color="white"
              @click="showDialog('HelloWorld')"
            >
              <v-icon left dark> mdi-store </v-icon>Sản phẩm
            </v-btn>
            <v-btn elevation="0" small class="rounded-0" color="primary">
              <v-icon left dark class="mx-0"> mdi-plus </v-icon>
            </v-btn>
          </div>
          <div class="d-inline-block elevation-2 ml-10">
            <v-btn
              elevation="0"
              small
              tile
              color="white"
              @click="showDialog('Login')"
            >
              <v-icon left dark> mdi-basket </v-icon> Phân Loại
            </v-btn>
            <v-btn elevation="0" small class="rounded-0" color="primary">
              <v-icon left dark class="mx-0"> mdi-plus </v-icon>
            </v-btn>
          </div>
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
        </v-col>
        <v-col class="d-flex flex-row-reverse col-md-8">
          <div class="d-inline-block elevation-2 ml-10">
            <v-btn elevation="0" small tile dark color="red">
              <v-icon centered dark class="mx-0"> mdi-power </v-icon>
            </v-btn>
          </div>
          <div class="d-inline-block elevation-2 ml-10">
            <v-btn elevation="0" small class="rounded-0" dark color="orange">
              <v-icon centered dark class="mx-0"> mdi-logout-variant </v-icon>
            </v-btn>
          </div>
          <v-btn small class="rounded-0" color="white elevation-2 ml-10">
            <v-icon left dark> mdi-account </v-icon> Admin
          </v-btn>
          <div
            class="d-inline-block elevation-2 ml-10"
            @click="showDialog('User')"
          >
            <v-btn elevation="0" small tile color="white">
              <v-icon left dark> mdi-account </v-icon> Tài khoản
            </v-btn>
            <v-btn elevation="0" small class="rounded-0" color="primary">
              <v-icon left dark class="mx-0"> mdi-plus </v-icon>
            </v-btn>
          </div>
          <v-btn
            small
            color="white"
            tile
            class="elevation-2 ml-10"
            @click="showDialog('Transcation')"
          >
            <v-icon left dark> mdi-card-account-details-outline </v-icon> Giao
            dịch
          </v-btn>
          <v-btn
            small
            color="white"
            tile
            class="elevation-2 ml-10"
            @click="showDialog('POS')"
          >
            <v-icon left dark> mdi-card-account-details-outline </v-icon> Point
            of Sale
          </v-btn>
          <v-btn
            small
            color="green"
            tile
            dark
            class="elevation-2 ml-10"
            @click="showScanDialog"
          >
            <v-icon centered dark> mdi-cog-outline </v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-container>

    <!-- Sizes your content based upon application components -->
    <v-main>
      <!-- Provides the application the proper gutter -->
      <v-container fluid>
        <!-- If using vue-router -->
        <router-view></router-view>
      </v-container>
    </v-main>

    <Dialog>
      <template v-slot:dialogBody>
        <keep-alive>
          <component :is="$store.state.dialogViewName"></component>
        </keep-alive>
      </template>
    </Dialog>

    <ScanDialog></ScanDialog>
  </v-app>
</template>

<script>
import Dialog from "../../components/Dialog.vue";
import ScanDialog from "../../components/ScanDialog.vue";
import Login from "./Login.vue";
import User from "../pages/User.vue";
import POS from "../pages/POS.vue";
import * as muType from "../../store/mutation-type";

export default {
  name: "Home",
  components: {
    Dialog,
    ScanDialog,
    Login,
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
    initialize() {
    },
  },
  created() {
    this.initialize();
  },
};
</script>


<style scoped>
#dashboard {
  background: transparent;
}
</style>