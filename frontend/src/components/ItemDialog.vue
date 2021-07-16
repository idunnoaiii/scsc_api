<template>
  <v-row justify="center">
    <v-dialog
      v-model="$store.state.itemDialog"
      max-width="80%"
      transition="dialog-bottom-transition"
      origin="center bottom"
    >
      <v-card>
        <v-card-title class="text-h5">
          <slot name="title"></slot>
        </v-card-title>
        <v-card-text>
          <slot name="dialogBody">
            <v-container
              class="d-flex align-content-lg-start"
              fluid
              fill-height
            >
              <v-row class="pa-1 align-center">
                <v-col cols="4">
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
                <v-col cols="1">
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
                <v-col cols="7">
                  <v-sheet tile class="py-4 px-1">
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
           
              <!-- <v-row class="m-5 pa-4"> -->
              <!-- <v-col
                  cols="2"
                  md="3"
                  sm="6"
                  lg="2"
                  v-for="item in items"
                  :key="item.id"
                > -->
              <div class="d-flex flex-row overflow-x-auto">
                <v-card
                  @click="addItemToOrder(item)"
                  v-for="item in items"
                  :key="item.id"
                  min-width="180px"
                  max-width="180px"
                  class="mx-1"
                  
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
                        class="
                          mb-2
                          primary--text
                          text--darken-2
                          font-weight-bold
                        "
                      >
                        {{ item.price }} VND
                      </v-list-item-title>
                      <v-list-item-subtitle class="text-truncate d-block">
                        {{ item.name }}
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-card>
              </div>
              <!-- </v-col> -->
              <!-- </v-row> -->
            </v-container>
          </slot>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue darken-1"
            text
            @click="$emit('delete-item-confirm')"
            >OK</v-btn
          >
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import axios from "../axios";

import { mapState, mapGetters, mapMutations, mapActions } from "vuex";
import _ from "lodash";

export default {
  data() {
    return {
      headers: [
        {
          text: "#",
          align: "start",
          sortable: false,
          value: "rownumber",
        },
        { text: "Item", value: "name" },
        { text: "Quantity", value: "quantity" },
        { text: "Price", value: "price" },
        { text: "", value: "actions", sortable: false },
      ],
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
    deleteItemConfirm() {
      this.closeDelete();
    },
    closeDelete() {
      this.showDialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assigcategories_selectedn(
          {},
          this.defaultItem
        );
        this.editedIndex = -1;
      });
    },

    enablePayDialog() {
      this.showPayDialog = true;
      console.log("ahihi");
    },

    closePayDialog() {
      this.showPayDialog = false;
    },

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