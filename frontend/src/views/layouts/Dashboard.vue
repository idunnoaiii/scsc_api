<template>
  <v-app>
    <v-container fluid class="my-2">
      <v-row>
        <v-col class="d-flex flex-row justify-start col-lg-6">
          <div class="d-inline-block elevation-2">
            <v-btn elevation="0" small class="rounded-0" color="white ">
              <v-icon left dark> mdi-store </v-icon>Sản phẩm
            </v-btn>
            <v-btn elevation="0" small class="rounded-0" color="primary">
              <v-icon left dark class="mx-0"> mdi-plus </v-icon>
            </v-btn>
          </div>
          <div class="d-inline-block elevation-2 ml-10">
            <v-btn elevation="0" small class="rounded-0" color="white ">
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
        <v-col class="d-flex flex-row-reverse">
          <div class="d-inline-block elevation-2 ml-10">
            <v-btn elevation="0" small class="rounded-0" dark color="red">
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
          <div class="d-inline-block elevation-2 ml-10">
            <v-btn elevation="0" small class="rounded-0" color="white">
              <v-icon left dark> mdi-account </v-icon> Tài khoản
            </v-btn>
            <v-btn elevation="0" small class="rounded-0" color="primary">
              <v-icon left dark class="mx-0"> mdi-plus </v-icon>
            </v-btn>
          </div>
          <v-btn small color="white" class="rounded-0 elevation-2 ml-10">
            <v-icon left dark> mdi-card-account-details-outline </v-icon> Giao dịch
          </v-btn>
          <v-btn small color="green" dark class="rounded-0 elevation-2 ml-10">
            <v-icon centered dark> mdi-cog-outline </v-icon>
          </v-btn>
        </v-col>

        <v-col cols="6"> </v-col>
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
  </v-app>
</template>

<script>
import vuetifyToast from "vuetify-toast";

export default {
  name: "Home",

  components: {},

  methods: {
    show: function () {
      vuetifyToast.success("Hello");
    },
  },
};
</script>
