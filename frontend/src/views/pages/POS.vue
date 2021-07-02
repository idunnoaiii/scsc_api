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
                <v-btn fab elevation-2 medium class="rounded-5" color="primary">
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
                  <v-icon small class="mr-2" @click="increaseQuantity(item)">
                    mdi-arrow-up-drop-circle-outline
                  </v-icon>
                  <v-icon small class="mr-2" @click="decreaseQuantity(item)">
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
                      <v-col cols="6"> : {{ this.totalItem }}</v-col>
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
                      <v-col cols="6"> : {{ this.grossPrice }} VND</v-col>
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
                    class="rounded-5 mr-lg-5 white--text"
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
                    color="#81c868"
                    @click="enablePayDialog"
                  >
                    <v-icon left dark class="mx-0" color="white"
                      >> mdi-cash
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
      v-on:confirm-payment="confirmPayment"
      v-bind:show="this.showPayDialog"
    >
    </PayDialog>
  </v-layout>
</template>

<script>
import axios from "../../axios";
import ConfirmDialog from "../../components/ConfirmDialog";
import PayDialog from "../../components/POS/PayDialog.vue";

export default {
  components: {
    ConfirmDialog,
    PayDialog,
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
      orderItems: [],
      items: [
        // {
        //   name: "Bánh chuối tròn",
        //   description: null,
        //   price: 20000,
        //   expired_date: null,
        //   image_url: null,
        //   quantity: null,
        //   category_id: null,
        //   stock: null,
        //   id: 1,
        //   is_active: true,
        // },
        // {
        //   name: "Bông lan trứng muối",
        //   description: null,
        //   price: 24000,
        //   expired_date: null,
        //   image_url: null,
        //   quantity: null,
        //   category_id: null,
        //   stock: null,
        //   id: 2,
        //   is_active: true,
        // },
        // {
        //   name: "Bánh Thỏi vàng",
        //   description: null,
        //   price: 14000,
        //   expired_date: null,
        //   image_url: null,
        //   quantity: null,
        //   category_id: null,
        //   stock: null,
        //   id: 3,
        //   is_active: true,
        // },
        // {
        //   name: "Bánh Mufin sữa",
        //   description: null,
        //   price: 25000,
        //   expired_date: null,
        //   image_url: null,
        //   quantity: null,
        //   category_id: null,
        //   stock: null,
        //   id: 4,
        //   is_active: true,
        // },
        // {
        //   name: "Bánh mì kem sữa",
        //   description: null,
        //   price: 25000,
        //   expired_date: null,
        //   image_url: null,
        //   quantity: null,
        //   category_id: null,
        //   stock: null,
        //   id: 5,
        //   is_active: true,
        // },
        // {
        //   name: "Bánh Tart phô mai",
        //   description: null,
        //   price: 20000,
        //   expired_date: null,
        //   image_url: null,
        //   quantity: null,
        //   category_id: null,
        //   stock: null,
        //   id: 6,
        //   is_active: true,
        // },
        // {
        //   name: "Bánh phô mai bơ tỏi",
        //   description: null,
        //   price: 20000,
        //   expired_date: null,
        //   image_url: null,
        //   quantity: null,
        //   category_id: null,
        //   stock: null,
        //   id: 7,
        //   is_active: true,
        // },
        // {
        //   name: "Bánh cade hột gà",
        //   description: null,
        //   price: 10000,
        //   expired_date: null,
        //   image_url: null,
        //   quantity: null,
        //   category_id: null,
        //   stock: null,
        //   id: 8,
        //   is_active: true,
        // },
        // {
        //   name: "Bánh Su kem",
        //   description: null,
        //   price: 15000,
        //   expired_date: null,
        //   image_url: null,
        //   quantity: null,
        //   category_id: null,
        //   stock: null,
        //   id: 9,
        //   is_active: true,
        // },
        // {
        //   name: "Bánh xúc xích phô mai",
        //   description: null,
        //   price: 10000,
        //   expired_date: null,
        //   image_url: null,
        //   quantity: null,
        //   category_id: null,
        //   stock: null,
        //   id: 10,
        //   is_active: true,
        // },
        // {
        //   name: "Bánh mi hạt sen",
        //   description: null,
        //   price: 30000,
        //   expired_date: null,
        //   image_url: null,
        //   quantity: null,
        //   category_id: null,
        //   stock: null,
        //   id: 11,
        //   is_active: true,
        // },
        // {
        //   name: "Bánh lột da hạt sen",
        //   description: null,
        //   price: 20000,
        //   expired_date: null,
        //   image_url: null,
        //   quantity: null,
        //   category_id: null,
        //   stock: null,
        //   id: 12,
        //   is_active: true,
        // },
        // {
        //   name: "Bánh mì táo đỏ",
        //   description: null,
        //   price: 25000,
        //   expired_date: null,
        //   image_url: null,
        //   quantity: null,
        //   category_id: null,
        //   stock: null,
        //   id: 13,
        //   is_active: true,
        // },
        // {
        //   name: "Bánh mini ngọt",
        //   description: null,
        //   price: 12000,
        //   expired_date: null,
        //   image_url: null,
        //   quantity: null,
        //   category_id: null,
        //   stock: null,
        //   id: 14,
        //   is_active: true,
        // },
        // {
        //   name: "Bánh bơ tỏi Pháp",
        //   description: null,
        //   price: 25000,
        //   expired_date: null,
        //   image_url: null,
        //   quantity: null,
        //   category_id: null,
        //   stock: null,
        //   id: 15,
        //   is_active: true,
        // },
        // {
        //   name: "string",
        //   description: "string",
        //   price: 0,
        //   expired_date: "2021-06-26T12:12:48.117000",
        //   image_url: "string",
        //   quantity: 0,
        //   category_id: null,
        //   stock: true,
        //   id: 18,
        //   is_active: true,
        // },
      ],
      categories:[],
      customerValue: 0,
      totalItem: 0,
      totalPrice: 0,
      grossPrice: 0,
      tax: 10,
      defaultItem: {},
      editedIndex: 0,
      showDialogDelete: false,
      showPayDialog: false,
    };
  },
  mounted() {
    this.$swal("hello");
    axios.get("/api/v1/items/all?skip=0&limit=100").then((response) => {
      this.items = response.data;
    });
    axios.get("/api/v1/categories").then((response) => {
      this.categories = response.data.map((item) => ({text : item.name, value: item.id}));
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
    initialize() {},
    getListItem() {
      axios.get("/api/v1/items/all?skip=0&limit=100").then((data) => {
        this.items = data.data;
      });
    },
    addItemToOrder(item) {
      let isNewItem = true;
      this.orderItems.forEach((orderItem) => {
        if (orderItem.id == item.id) {
          orderItem.quantity++;
          isNewItem = false;
          return;
        }
      });

      if (isNewItem) {
        let orderItem = {
          id: item.id,
          rownumber: this.orderItems.length + 1,
          name: item.name,
          quantity: 1,
          price: item.price,
        };

        this.orderItems.push(orderItem);
      }
      this.caculateTotalPrice();
    },
    caculateTotalPrice() {
      let totalItem = 0;
      let totalPrice = 0;
      for (let index = 0; index < this.orderItems.length; index++) {
        let item = this.orderItems[index];
        item.rownumber = index + 1;
        totalItem += item.quantity;
        totalPrice += item.quantity * item.price;
      }

      this.totalItem = totalItem;
      this.totalPrice = totalPrice;
      this.grossPrice = totalPrice;
    },
    deleteItem(item) {
      console.log(item);
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
            this.caculateTotalPrice();
            // this.$swal.fire("Deleted!", "Your file has been deleted.", "success");
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
    increaseQuantity(item) {
      item.quantity++;
      this.caculateTotalPrice();
    },
    decreaseQuantity(item) {
      if (item.quantity > 1) {
        item.quantity--;
        this.caculateTotalPrice();
      } else this.deleteItem(item);
    },
    enablePayDialog() {
      this.showPayDialog = true;
      console.log("ahihi");
    },
    closePayDialog() {
      this.showPayDialog = false;
    },
    confirmPayment(payload) {

      let orderDetail = {
        code: new Date().getTime(),
        user_id: 1,
        status: true,
        tax: 0,
        subtotal: this.totalPrice,
        paid: payload.amount,
        change: payload.change,
        order_items: [
          {
            item_id: 0,
            price: 0,
            quantity: 0,
            item_name: "string",
          },
        ],
      };

      orderDetail.order_items = this.orderItems.map((item) => ({
        item_id: item.id,
        price: item.price,
        quantity: item.quantity,
        item_name: item.name,
      }));

      axios
        .post("/api/v1/orders/", orderDetail)
        .then((response) => {
          console.log(response);
        })
        .catch((err) => {
          console.log(err);
        });
        
    },
    blurCustomer() {
      console.log(this.customerValue);
      if (this.customerValue) return;
      this.customerValue = this.customers[0];
    },
    clearOrderItem() {
      this.orderItems = [];
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