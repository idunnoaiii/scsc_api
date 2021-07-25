<template>
  <v-layout>
    <v-col lg="4">
      <v-card outlined height="100%">
        <v-container fill-height class="d-flex">
          <v-row class="mt-1 align-self-start" justify="center">
            <v-row class="mx-3 mb-2 elevation-0 justify-center">
              <!-- <v-col cols="4">
                  <span class="text-h5" style="color: grey">Order: #123</span>
                </v-col>
                <v-divider class="mx-4" inset vertical></v-divider> -->

              <!-- <v-col cols="10">
                <v-chip-group
                  mandatory
                  active-class="primary"
                  v-model="currentTab"
                >
                  <v-chip
                    v-for="hold in listOnHold"
                    :key="hold.value"
                    :value="hold.value"
                    close
                    @click:close="removeOnHold(hold.value)"
                  >
                    {{ hold.text }}
                  </v-chip>
                </v-chip-group>
              </v-col>
              <v-col cols="2">
                <v-btn
                  fab
                  @click="addOnHold"
                  :disabled="listOnHold.length == 20"
                  color="green"
                  dark
                >
                  +
                </v-btn>
              </v-col> -->
              <v-col cols="12" class="text-h5">
                Order #{{this.currentOrderCode}}
              </v-col>
            </v-row>
            <v-data-table
              :headers="headers"
              :items="orderItems"
              class="elevation-4 mx-3"
            >
              <template v-slot:[`item.quantity`]="props">
                <v-edit-dialog>
                  {{ props.item.quantity }}
                  <template v-slot:input>
                    <v-text-field
                      v-model="props.item.quantity"
                      @change="
                        updateItemQuantity({
                          quantity: props.item.quantity,
                          itemId: props.item.id,
                        })
                      "
                      label="Edit"
                      single-line
                      counter
                      min="1"
                      type="number"
                      step="1"
                    ></v-text-field>
                  </template>
                </v-edit-dialog>
              </template>
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
                <v-icon small color="red darken-1" @click="deleteItem(item.id)">
                  mdi-delete
                </v-icon>
              </template>
            </v-data-table>
          </v-row>
          <v-row class="align-self-end my-0">
            <v-card width="100%" class="mx-3 elevation-6">
              <v-container fluid>
                <v-row class="mb-4">
                  <v-col cols="6">
                    <v-row>
                      <v-col cols="6" class=""> Total Items(s) </v-col>
                      <v-col cols="6"> : {{ this.totalOrderItem }}</v-col>
                    </v-row>
                    <v-row>
                      <v-col cols="6"> Subtotal </v-col>
                      <v-col cols="6">
                        : {{ this.totalPrice | currency }} VND</v-col
                      >
                    </v-row>
                  </v-col>
                  <v-col cols="6">
                    <v-row>
                      <v-col cols="6"> Subtotal </v-col>
                      <v-col cols="6">
                        : {{ this.totalPrice | currency }} VND</v-col
                      >
                    </v-row>
                    <v-row>
                      <v-col cols="6"> Total </v-col>
                      <v-col cols="6">
                        : {{ this.totalPrice | currency }} VND</v-col
                      >
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
            <v-col cols="3">
              <v-autocomplete
                :items="customers"
                @blur="blurCustomer"
                v-model="customerValue"
                auto-select-first
                clearable
                deletable-chips
                hide-details
                label="Customer"
                outlined
                dense
              ></v-autocomplete>
            </v-col>
            <!-- <v-col cols="2">
              <v-btn
                fab
                elevation-2
                medium
                class="rounded-5"
                color="primary"
                @click="$store.commit('SHOW_GLOBAL_DIALOG', 'AddCustomer')"
              >
                <v-icon left dark class="mx-0"> mdi-plus </v-icon>
              </v-btn>
            </v-col> -->

            <v-col cols="4">
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
            <v-col cols="4">
              <v-text-field
                outlined
                label="Search item by name"
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
                class="rounded-5 white--text"
                @click="clearSearch"
                color="primary"
              >
                Clear
              </v-btn>
            </v-col>
          </v-row>
          <v-row>
            <v-divider></v-divider>
          </v-row>
          <v-row
            v-show="!$store.state.scanMode"
            style="overflow-y: scroll; max-height: 726px"
          >
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
                      {{ item.price | currency }} VND
                    </v-list-item-title>
                    <v-list-item-subtitle class="text-truncate d-block">
                      {{ item.name }}
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-card>
            </v-col>
          </v-row>
          <!-- <v-row>
            <div class="justify-center">
              <v-pagination v-model="page" :length="6"></v-pagination>
            </div>
          </v-row> -->
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
    this.getCustomer();
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
      updateItemQuantity: "UPDATE_ITEM_QUANTITY",
      deleteItem: "DELETE_ITEM_ORDER",
      addOnHold: "ADD_ON_HOLD",
      removeOnHold: "REMOVE_ON_HOLD",
      blurCustomer: "BLUR_CUSTOMER",
    }),
    ...mapActions("POS", {
      checkout: "checkout",
      getCustomer: "getCustomer",
      updateCurrentTab: "updateCurrentTab",
      changeCustomerValue: "changeCustomerValue",
    }),
  },
  computed: {
    ...mapState("POS", {
      orderItems: "orderItems",
      showBillDialog: "showBillDialog",
      customers: "customers",
      listOnHold: "listOnHold",
      currentOrderCode: "currentOrderCode"
    }),
    ...mapGetters("POS", {
      totalOrderItem: "totalOrderItem",
      totalPrice: "totalPrice",
    }),
    currentTab: {
      get() {
        return this.$store.state.POS.currentTab;
      },
      set(value) {
        return this.updateCurrentTab(value);
      },
    },
    customerValue: {
      get() {
        return this.$store.state.POS.customerValue;
      },
      set(value) {
        this.changeCustomerValue(value);
      },
    },
  },

  watch: {
    searchCriteria: {
      handler: function (newValue) {
        if (newValue) this.handlerSearch();
      },
      deep: true,
    },
  },

  filters: {
    currency(value) {
      return value.toLocaleString();
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