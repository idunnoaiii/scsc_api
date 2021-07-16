<template>
  <v-layout>
    <v-col lg="4">
      <v-card outlined height="100%">
        <v-container fill-height class="d-flex align-baseline">
          <div>
            <v-row class="mt-4">
              <v-data-table
                :headers="headers"
                :items="orderItems"
                class="elevation-4 mx-6"
              >
                <!-- <template v-slot:[`item.quantity`]="props">
                  <v-edit-dialog
                    :return-value.sync="props.item.quantity"
                    @cancel="cancel"
                    @open="open"
                    @close="close"
                  >
                    {{ props.item.quantity }}
                    <template v-slot:input>
                      <v-text-field
                        v-model="props.item.quantity"
                        label="Edit"
                        single-line
                        counter
                        type="number"
                        step="1"
                      ></v-text-field>
                    </template>
                  </v-edit-dialog>
                </template> -->
                <template v-slot:[`item.actions`]="{ item }">
                  <v-icon
                    small
                    color="green darken-1"
                    class="mr-2"
                    @click="increaseQuantity(item.id)"
                  >
                    mdi-arrow-up-drop-circle-outline
                  </v-icon>
                  <v-icon
                    small
                    color="orange darken-1"
                    class="mr-2"
                    @click="decreaseQuantity(item.id)"
                  >
                    mdi-arrow-down-drop-circle-outline
                  </v-icon>
                  <v-icon
                    small
                    color="red darken-1"
                    @click="deleteItem(item.id)"
                  >
                    mdi-delete
                  </v-icon>
                </template>
              </v-data-table>
            </v-row>
          </div>

          <v-row class="align-self-end my-0">
            <v-card width="100%" class="mx-6 elevation-6">
              <v-container fluid>
                <v-row class="mb-4">
                  <v-col cols="6">
                    <v-row>
                      <v-col cols="6" class=""> Total Items(s) </v-col>
                      <v-col cols="6"> : {{ this.totalOrderItem }}</v-col>
                    </v-row>
                  </v-col>
                  <v-col cols="6">
                    <v-row>
                      <v-col cols="6"> Price </v-col>
                      <v-col cols="6"> : {{ this.totalPrice }} VND</v-col>
                    </v-row>
                    <v-row>
                      <v-col cols="6"> Gross Price </v-col>
                      <v-col cols="6"> : {{ this.totalPrice }} VND</v-col>
                    </v-row>
                  </v-col>
                </v-row>
                <v-row class="mb-2 mx-auto">
                  <v-spacer></v-spacer>
                  <!-- <v-btn
                    elevation="0"
                    small
                    class="rounded-5 mr-lg-5"
                    color="#34d3eb"
                  >
                    <v-icon left bright class="mx-0" color="white">
                      mdi-printer
                    </v-icon>
                  </v-btn> -->
                  <v-btn
                    elevation="4"
                    class="rounded-5 mr-lg-5 white--text"
                    color="red darken-1"
                    @click="clearOrderItem"
                  >
                    <v-icon left dark class="mx-0" color="white"
                      >> mdi-cancel
                    </v-icon>
                    <span class="hidden-sm-and-down ml-3">Clear</span>
                  </v-btn>
                  <v-btn
                    elevation="4"
                    small
                    class="rounded-5 mr-lg-5 white--text d-none"
                    color="#5fbeaa"
                  >
                    <v-icon left dark class="mx-0 white--text" color="white"
                      >> mdi-hand
                    </v-icon>
                    <span class="hidden-sm-and-down ml-3">Hold</span>
                  </v-btn>
                  <v-btn
                    elevation="4"
                    class="rounded-5 white--text"
                    color="green darken-1"
                    @click="$store.commit('SET_PAYDIALOG', true)"
                    :disabled="this.orderItems.length == 0"
                  >
                    <v-icon left dark class="mx-0" color="white">
                      mdi-cash
                    </v-icon>
                    <span class="hidden-sm-and-down ml-3">Pay</span>
                  </v-btn>
                </v-row>
              </v-container>
            </v-card>
          </v-row>
        </v-container>
      </v-card>
    </v-col>
    <v-col lg="8">
      <v-card class="" height="100%" outlined tile>
        <v-container class="d-flex align-content-lg-start" fluid fill-height>
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
          <v-row>
            <v-divider></v-divider>
          </v-row>
          <v-row class="m-5 pa-4" v-show="!$store.state.scanMode">
            <v-col
              cols="2"
              md="3"
              sm="6"
              lg="2"
              v-for="item in items"
              :key="item.id"
            >
              <v-card @click="addItemToOrder(item)">
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
          <v-row class="pa-1 align-center" v-show="$store.state.scanMode">
            <Scanning />
          </v-row>
        </v-container>
      </v-card>
    </v-col>
    <!-- <keep-alive>
      <v-col lg="8">
        <v-card class="" height="100%" outlined tile>
          <v-container class="d-flex align-content-lg-start" fluid fill-height>
          </v-container>
        </v-card>
      </v-col>
    </keep-alive> -->
    <ConfirmDialog
      v-on:close-payment-dialog="closeDelete()"
      v-on:delete-item-confirm="deleteItemConfirm()"
      v-bind:showDialog="this.showDialogDelete"
    >
      <template v-slot:title="">
        <v-btn>Delete</v-btn>
      </template>
    </ConfirmDialog>

    <PayDialog v-on:confirm-payment="checkout" v-if="$store.state.payDialog">
    </PayDialog>
    <BillDialog v-bind:show="this.showBillDialog"> </BillDialog>
  </v-layout>
</template>

<script>
import axios from "../../axios";
import ConfirmDialog from "../../components/ConfirmDialog";
import PayDialog from "../../components/POS/PayDialog.vue";
import BillDialog from "../../components/BillDialog.vue";
import Scanning from "../../components/Scanning.vue";
import { mapState, mapGetters, mapMutations, mapActions } from "vuex";
import _ from "lodash";

export default {
  components: {
    ConfirmDialog,
    PayDialog,
    BillDialog,
    Scanning,
  },
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
      this.$store.commit("SET_SCAN_MODE", false);
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