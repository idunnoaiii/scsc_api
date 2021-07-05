<template>
  <v-layout>
    <v-col lg="4">
      <v-card outlined height="100%">
        <v-container fill-height class="d-flex align-baseline">
          <div>
            <v-row>
              <v-col cols="9" class="ml-4">
                <v-autocomplete
                  :items="customers"
                  @blur="blurCustomer"
                  v-model="customerValue"
                  auto-select-first
                  clearable
                  deletable-chips
                  hide-details
                  solo
                ></v-autocomplete>
              </v-col>
              <v-col cols="2">
                <v-btn
                  fab
                  elevation-2
                  medium
                  class="rounded-5"
                  color="primary"
                  @click="setBillDialog(true)"
                >
                  <v-icon left dark class="mx-0"> mdi-plus </v-icon>
                </v-btn>
              </v-col>
            </v-row>
            <v-row class="mt-4">
              <v-data-table
                :headers="headers"
                :items="orderItems"
                class="elevation-4 mx-6"
              >
                <template v-slot:[`item.actions`]="{ item }">
                  <v-icon small class="mr-2" @click="increaseQuantity(item.id)">
                    mdi-arrow-up-drop-circle-outline
                  </v-icon>
                  <v-icon small class="mr-2" @click="decreaseQuantity(item.id)">
                    mdi-arrow-down-drop-circle-outline
                  </v-icon>
                  <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
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
                      <v-col cols="6">
                        Gross Price (inc {{ this.tax }}% Tax)
                      </v-col>
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
                    small
                    class="rounded-5 mr-lg-5 white--text"
                    color="red"
                    @click="clearOrderItem"
                  >
                    <v-icon left dark class="mx-0" color="white"
                      >> mdi-cancel
                    </v-icon>
                    <span class="hidden-sm-and-down ml-3">Cancel</span>
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
                    small
                    class="rounded-5 white--text"
                    color="green"
                    @click="enablePayDialog"
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
          <v-row class="m-5 pa-5 align-center">
            <v-col cols="4">
              <v-text-field
                solo
                label="Search product by name or sku"
                clearable
                width="200px"
                hide-details
              ></v-text-field>
            </v-col>
            <v-col cols="1">
              <v-btn
                elevation="4"
                big
                class="rounded-5 ml-2 white--text"
                color="primary"
              >
                <v-icon>mdi-text-box-search-outline</v-icon>
              </v-btn>
            </v-col>
            <v-col cols="7">
              <v-sheet tile class="py-4 px-1">
                <v-chip-group multiple active-class="primary--text">
                  <v-chip v-for="cate in categories" :key="cate.value">
                    {{ cate.text }}
                  </v-chip>
                </v-chip-group>
              </v-sheet>
            </v-col>
          </v-row>
          <v-divider class="pa-2"></v-divider>
          <v-row class="m-5 pa-5">
            <v-card
              v-for="item in items"
              :key="item.id"
              class="ma-2 d-flex flex-column"
              @click="addItemToOrder(item)"
            >
              <!-- <v-img
              class="ma-1 item-img"
              height="120"
              width="120"
              src="https://cdn.vuetifyjs.com/images/cards/cooking.png"
            ></v-img> -->
              <img
                src="https://cdn.vuetifyjs.com/images/cards/cooking.png"
                class="item-img"
                alt=""
              />

              <v-card-title
                class="
                  text-center text-body-2
                  pa-1
                  mt-1
                  item-name-text
                  darkgrey--text
                "
              >
                {{ item.name }}
              </v-card-title>
              <v-divider class="mx-2"></v-divider>

              <v-card-text
                class="
                  font-weight-medium
                  text-center text-subtitle-1
                  pa-0
                  green--text
                  align-item-end
                "
              >
                {{ item.price }} VND
              </v-card-text>
            </v-card>
          </v-row>
        </v-container>
      </v-card>
    </v-col>
    <ConfirmDialog
      v-on:close-payment-dialog="closeDelete()"
      v-on:delete-item-confirm="deleteItemConfirm()"
      v-bind:showDialog="this.showDialogDelete"
    >
      <template v-slot:title="">
        <v-btn>Delete</v-btn>
      </template>
    </ConfirmDialog>

    <PayDialog
      v-on:close-payment-dialog="closePayDialog()"
      v-on:confirm-payment="checkout"
      v-bind:show="this.showPayDialog"
    >
    </PayDialog>
    <BillDialog v-bind:show="this.showBillDialog"> </BillDialog>
  </v-layout>
</template>

<script>
import axios from "../../axios";
import ConfirmDialog from "../../components/ConfirmDialog";
import PayDialog from "../../components/POS/PayDialog.vue";
import BillDialog from "../../components/BillDialog.vue";
import { mapState, mapGetters, mapMutations, mapActions } from "vuex";

export default {
  components: {
    ConfirmDialog,
    PayDialog,
    BillDialog,
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
      customers: [],
      items: [],
      categories: [],
      customerValue: 0,
      grossPrice: 0,
      tax: 10,
      defaultItem: {},
      editedIndex: 0,
      showDialogDelete: false,
      showPayDialog: false,
    };
  },
  mounted() {
    axios.get("/api/v1/items/all?skip=0&limit=100").then((response) => {
      this.items = response.data;
    });
    axios.get("/api/v1/categories").then((response) => {
      this.categories = response.data.map((item) => ({
        text: item.name,
        value: item.id,
      }));
    });
    axios.get("/api/v1/customers").then((response) => {
      this.customers = response.data.map((item) => ({
        text: `${item.phone} - ${item.name}`,
        value: item.phone,
      }));
      this.customers.unshift({ text: "Walk in customer", value: -1 });
      this.customerValue = this.customers[0];
    });
  },
  methods: {
    deleteItem(item) {
      this.$swal
        .fire({
          title: "Are you sure?",
          text: "You won't be able to revert this!",
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Yes, delete it!",
        })
        .then((result) => {
          if (result.isConfirmed) {
            this.editedIndex = this.orderItems.indexOf(item);
            this.orderItems.splice(this.editedIndex, 1);
          }
        });
    },
    deleteItemConfirm() {
      this.closeDelete();
    },
    closeDelete() {
      this.showDialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
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
    blurCustomer() {
      console.log(this.customerValue);
      if (this.customerValue) return;
      this.customerValue = this.customers[0];
    },
    clearOrderItem() {
      // this.orderItems = [];
    },
    ...mapMutations("POS", {
      addItemToOrder: "ADD_ITEM_TO_ORDER",
      clearOrderItem: "CLEAR_ORDER_ITEM",
      setBillDialog: "SET_BILL_DIALOG",
      increaseQuantity: "INCREASE_ITEM_QUANTITY",
      decreaseQuantity: "DECREASE_ITEM_QUANTITY"
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
  },
};
</script>


<style scoped>
.h-min-85vh {
  min-height: 65vh !important;
}
.fontsize-13 {
  font-size: 13px !important;
}
.item-name-text {
  word-wrap: break-word;
  max-width: 120px;
}

.item-img {
  height: 120px !important;
  width: 120px !important;
}

.swal2-popup.swal2-modal.swal2-icon-warning.swal2-show {
  font-family: "Roboto", sans-serif;
}
</style>