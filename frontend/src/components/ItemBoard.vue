<template>
  <v-row justify="center">
    <v-card elevation="0">
      <v-card-text v-if="capturedItemPicked != null">
        <v-container class="d-flex align-content-lg-start" fluid>
          <v-row>
            <v-col cols="5" class="col-offset-2">
              <img
                :src="
                  capturedItemPicked.image_url != null
                    ? capturedItemPicked.image_url
                    : 'https://storage.googleapis.com/scscbakery.appspot.com/no-image.png'
                "
                alt="image"
                min-height="180px"
                max-height="200px"
                height="200px"
              />
            </v-col>
            <v-col cols="7">
              <v-list-item three-line>
                <v-list-item-content>
                  <v-list-item-title
                    class="
                      mb-2
                      primary--text
                      text--darken-2 text-h5
                      font-weight-bold
                    "
                  >
                    {{ capturedItemPicked.price }} VND
                  </v-list-item-title>
                  <v-list-item-subtitle class="text-truncate d-block text-h6">
                    {{ capturedItemPicked.name }}
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-col>
          </v-row>
        </v-container>

        <!-- <v-card
          @click="addItemToOrder(items[0])"
          min-width="180px"
          max-width="180px"
        >
          <v-list-item three-line>
            <v-list-item-content>
              <div class="mb-2" style="min-height: 140px">
                <img
                  :src="
                    items[0].image_url != null
                      ? items[0].image_url
                      : 'https://storage.googleapis.com/scscbakery.appspot.com/no-image.png'
                  "
                  class="item-img"
                  alt="image"
                  max-height="120px"
                />
              </div>
              <v-list-item-title
                class="mb-2 primary--text text--darken-2 font-weight-bold"
              >
                {{ items[0].price }} VND
              </v-list-item-title>
              <v-list-item-subtitle class="text-truncate d-block">
                {{ items[0].name }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-card> -->
        <v-row>
          <v-divider class="my-8"></v-divider>
        </v-row>
      </v-card-text>
      <v-card-text>
        <v-container class="d-flex align-content-lg-start" fluid fill-height>
          <v-row class="pa-1 align-center">
            <v-col cols="10">
              <v-text-field
                solo
                label="Search"
                clearable
                width="200px"
                hide-details
                :value="searchCriteria.searchValue"
                @input="inputSearchDelay"
              ></v-text-field>
            </v-col>
            <v-col cols="2">
              <v-btn
                elevation="4"
                big
                class="rounded-5 ml-2 white--text"
                @click="clearSearch"
                color="primary"
              >
                Clear
              </v-btn>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-sheet tile class="py-1 px-1">
                <v-chip-group
                  multiple
                  active-class="primary--text"
                  v-model="searchCriteria.categories_selected"
                >
                  <v-chip
                    v-for="cate in categories"
                    :key="cate.value"
                    :value="cate.value"
                  >
                    {{ cate.text }}
                  </v-chip>
                </v-chip-group>
              </v-sheet>
            </v-col>
          </v-row>
          <v-row class="px-1" style="max-height: 480px; overflow-y: scroll">
            <v-col cols="4" md="6" lg="4" v-for="item in items" :key="item.id">
              <v-card
                @click="changeCapturedItemPick(item)"
                min-width="180px"
                max-width="180px"
              >
                <v-list-item three-line>
                  <v-list-item-content>
                    <div class="mb-2" style="min-height: 140px">
                      <img
                        :src="
                          item.image_url != null
                            ? item.image_url
                            : 'https://storage.googleapis.com/scscbakery.appspot.com/no-image.png'
                        "
                        class="item-img"
                        alt="image"
                        max-height="120px"
                      />
                    </div>
                    <v-list-item-title
                      class="mb-2 primary--text text--darken-2 font-weight-bold"
                    >
                      {{ item.price }} VND
                    </v-list-item-title>
                    <v-list-item-subtitle class="text-truncate d-block">
                      {{ item.name }}
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
  </v-row>
</template>

<script>
import axios from "../axios";

import { mapState, mapGetters, mapMutations, mapActions } from "vuex";
import _ from "lodash";

export default {
  data() {
    return {
      items: [],
      categories: [],
      grossPrice: 0,
      tax: 10,
      defaultItem: {},
      editedIndex: 0,
      showDialogDelete: false,
      searchCriteria: {
        searchValue: "",
        categories_selected: [],
      },
    };
  },
  created() {
    axios.get("/api/v1/items/all?skip=0&limit=100").then((response) => {
      this.items = response.data;
    });
    axios.get("/api/v1/categories").then((response) => {
      this.categories = response.data.map((item) => ({
        text: item.name,
        value: item.id,
      }));
    });
  },
  methods: {
    // deleteItem(item) {
    //   // this.$swal
    //   //   .fire({
    //   //     title: "Are you sure?",
    //   //     text: "You won't be able to revert this!",
    //   //     icon: "warning",
    //   //     showCancelButton: true,
    //   //     confirmButtonColor: "#3085d6",
    //   //     cancelButtonColor: "#d33",
    //   //     confirmButtonText: "Yes, delete it!",
    //   //   })
    //   //   .then((result) => {
    //   //     if (result.isConfirmed) {
    //   //     }
    //   //   });
    //   this.editedIndex = this.orderItems.indexOf(item);
    //   this.orderItems.splice(this.editedIndex, 1);
    // },

    handlerSearch() {
      axios
        .post("/api/v1/items/search", this.searchCriteria)
        .then((response) => {
          this.items = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    clearSearch() {
      this.searchCriteria.searchValue = "";
      this.searchCriteria.categories_selected = [];
      this.handlerSearch();
    },

    inputSearchDelay: _.debounce(function (e) {
      this.searchCriteria.searchValue = e;
    }, 300),

    ...mapMutations("POS", {
      addItemToOrder: "ADD_ITEM_TO_ORDER",
      clearOrderItem: "CLEAR_ORDER_ITEM",
      setBillDialog: "SET_BILL_DIALOG",
      increaseQuantity: "INCREASE_ITEM_QUANTITY",
      decreaseQuantity: "DECREASE_ITEM_QUANTITY",
      deleteItem: "DELETE_ITEM_ORDER",
    }),
    ...mapMutations({
        changeCapturedItemPick: "CHANGE_CAPTURED_ITEM_PICK"
    }),
    ...mapActions("POS", {
      checkout: "checkout",
    }),
  },
  computed: {
    ...mapState("POS", {
      orderItems: "orderItems",
      showBillDialog: "showBillDialog",
      checkoutStatus: "checkoutStatus",
    }),

    ...mapState({
      capturedItemPicked: "capturedItemPicked",
    }),

    ...mapGetters("POS", {
      totalOrderItem: "totalOrderItem",
      totalPrice: "totalPrice",
    }),
  },

  watch: {
    checkoutStatus: function (newValue) {
      if (newValue == true) {
        this.$swal.fire({
          icon: "success",
          title: "Checkout successfully",
        });
        this.showPayDialog = false;
      }
    },
    searchCriteria: {
      handler: function (newValue) {
        if (newValue) this.handlerSearch();
      },
      deep: true,
    },
  },
};
</script>


<style scoped>
/* .h-min-85vh {
  min-height: 65vh !important;
}
.fontsize-13 {
  font-size: 13px !important;
}
.item-name-text {
  word-wrap: break-word;
  max-width: 120px;
}
*/

.item-img {
  max-height: 140px;
  width: 100%;
}

.swal2-popup.swal2-modal.swal2-icon-warning.swal2-show {
  font-family: "Roboto", sans-serif;
}
</style>