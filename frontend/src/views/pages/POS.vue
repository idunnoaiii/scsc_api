<template>
  <v-container class="grey lighten-5" fluid fill-height>
    <v-layout>
      <v-col lg="4">
        <v-card class="pa-2 h-min-85vh" outlined tile>
          <v-row>
            <v-col cols="9">
              <v-select
                :items="customers"
                label="Walk in customer"
                dense
                outlined
              ></v-select>
            </v-col>
            <v-col cols="3">
              <v-btn elevation="0" big class="rounded-5" color="green">
                <v-icon left dark class="mx-0"> mdi-plus </v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-row>
            <v-data-table
              :headers="headers"
              :items="orderItems"
              :items-per-page="10"
              class="elevation-1 ma-5"
            >
              <template v-slot:item.actions="{ item }">
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
        </v-card>
        <v-footer padless class="font-weight-medium fontsize-13">
          <v-col class="text-center" cols="12">
            <v-row>
              <v-col cols="6">
                <v-row>
                  <v-col cols="6"> Total Items(s) </v-col>
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
            <v-row class="mb-5 mr-5">
              <v-spacer></v-spacer>
              <v-btn
                elevation="0"
                small
                class="rounded-5 mr-lg-5"
                color="#34d3eb"
              >
                <v-icon left bright class="mx-0" color="white">
                  mdi-printer
                </v-icon>
              </v-btn>
              <v-btn
                elevation="0"
                small
                class="rounded-5 mr-lg-5"
                color="#f05050"
              >
                <v-icon left dark class="mx-0" color="white"
                  >> mdi-cancel
                </v-icon>
                <span class="hidden-sm-and-down ml-3">Cancel</span>
              </v-btn>
              <v-btn
                elevation="0"
                small
                class="rounded-5 mr-lg-5"
                color="#5fbeaa"
              >
                <v-icon left dark class="mx-0" color="white"
                  >> mdi-hand
                </v-icon>
                <span class="hidden-sm-and-down ml-3">Hold</span>
              </v-btn>
              <v-btn
                elevation="0"
                small
                class="rounded-5"
                color="#81c868"
                @click="enablePayDialog()"
              >
                <v-icon left dark class="mx-0" color="white"
                  >> mdi-cash
                </v-icon>
                <span class="hidden-sm-and-down ml-3">Pay</span>
              </v-btn>
            </v-row>
          </v-col>
        </v-footer>
      </v-col>
      <v-col lg="8">
        <v-card class="pa-2" outlined tile>
          <v-row class="m-5 pa-5 align-center">
            <v-text-field label="Search product by name or sku"></v-text-field>

            <v-btn elevation="0" big class="rounded-5 ml-2" color="#81c868">
              <span class="hidden-sm-and-down">All</span>
            </v-btn>
          </v-row>
          <v-divider class="pa-2"></v-divider>
          <v-row class="m-5 pa-5">
            <v-card
              v-for="item in items"
              :key="item.id"
              class="ma-2"
              @click="addItemToOrder(item)"
            >
              <v-img
                class="ma-3 rounded-circle"
                height="100"
                width="100"
                src="https://cdn.vuetifyjs.com/images/cards/cooking.png"
              ></v-img>

              <v-card-text
                class="
                  font-weight-medium
                  text-center text-subtitle-1
                  pa-0
                  mt-2
                  item-name-text
                "
              >
                {{ item.name }}
              </v-card-text>
              <v-divider class="mx-4"></v-divider>

              <v-card-text
                class="
                  font-weight-medium
                  text-center text-subtitle-1
                  pa-0
                  green--text
                "
              >
                {{ item.price }} VND
              </v-card-text>
            </v-card>
          </v-row>
        </v-card>
      </v-col>
      <DialogDeleteItem
        v-on:close-delete="closeDelete()"
        v-on:delete-item-confirm="deleteItemConfirm()"
        v-bind:showDialog="this.showDialogDelete"
      >
      </DialogDeleteItem>
      <PayDialog
        v-on:close-delete="closePayDialog()"
        v-bind:enableDialog="this.showPayDialog"
      >
      </PayDialog>
    </v-layout>
  </v-container>
</template>

<script>
import axios from "../../axios";
import DialogDeleteItem from "../../components/DialogDeleteItem";
import PayDialog from "../../components/POS/PayDialog";

export default {
  components: {
    DialogDeleteItem,
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
      orderItems: [],
      items: [
        {
          name: "Bánh chuối tròn",
          description: null,
          price: 20000,
          expired_date: null,
          image_url: null,
          quantity: null,
          category_id: null,
          stock: null,
          id: 1,
          is_active: true,
        },
        {
          name: "Bông lan trứng muối",
          description: null,
          price: 24000,
          expired_date: null,
          image_url: null,
          quantity: null,
          category_id: null,
          stock: null,
          id: 2,
          is_active: true,
        },
        {
          name: "Bánh Thỏi vàng",
          description: null,
          price: 14000,
          expired_date: null,
          image_url: null,
          quantity: null,
          category_id: null,
          stock: null,
          id: 3,
          is_active: true,
        },
        {
          name: "Bánh Mufin sữa",
          description: null,
          price: 25000,
          expired_date: null,
          image_url: null,
          quantity: null,
          category_id: null,
          stock: null,
          id: 4,
          is_active: true,
        },
        {
          name: "Bánh mì kem sữa",
          description: null,
          price: 25000,
          expired_date: null,
          image_url: null,
          quantity: null,
          category_id: null,
          stock: null,
          id: 5,
          is_active: true,
        },
        {
          name: "Bánh Tart phô mai",
          description: null,
          price: 20000,
          expired_date: null,
          image_url: null,
          quantity: null,
          category_id: null,
          stock: null,
          id: 6,
          is_active: true,
        },
        {
          name: "Bánh phô mai bơ tỏi",
          description: null,
          price: 20000,
          expired_date: null,
          image_url: null,
          quantity: null,
          category_id: null,
          stock: null,
          id: 7,
          is_active: true,
        },
        {
          name: "Bánh cade hột gà",
          description: null,
          price: 10000,
          expired_date: null,
          image_url: null,
          quantity: null,
          category_id: null,
          stock: null,
          id: 8,
          is_active: true,
        },
        {
          name: "Bánh Su kem",
          description: null,
          price: 15000,
          expired_date: null,
          image_url: null,
          quantity: null,
          category_id: null,
          stock: null,
          id: 9,
          is_active: true,
        },
        {
          name: "Bánh xúc xích phô mai",
          description: null,
          price: 10000,
          expired_date: null,
          image_url: null,
          quantity: null,
          category_id: null,
          stock: null,
          id: 10,
          is_active: true,
        },
        {
          name: "Bánh mi hạt sen",
          description: null,
          price: 30000,
          expired_date: null,
          image_url: null,
          quantity: null,
          category_id: null,
          stock: null,
          id: 11,
          is_active: true,
        },
        {
          name: "Bánh lột da hạt sen",
          description: null,
          price: 20000,
          expired_date: null,
          image_url: null,
          quantity: null,
          category_id: null,
          stock: null,
          id: 12,
          is_active: true,
        },
        {
          name: "Bánh mì táo đỏ",
          description: null,
          price: 25000,
          expired_date: null,
          image_url: null,
          quantity: null,
          category_id: null,
          stock: null,
          id: 13,
          is_active: true,
        },
        {
          name: "Bánh mini ngọt",
          description: null,
          price: 12000,
          expired_date: null,
          image_url: null,
          quantity: null,
          category_id: null,
          stock: null,
          id: 14,
          is_active: true,
        },
        {
          name: "Bánh bơ tỏi Pháp",
          description: null,
          price: 25000,
          expired_date: null,
          image_url: null,
          quantity: null,
          category_id: null,
          stock: null,
          id: 15,
          is_active: true,
        },
        {
          name: "string",
          description: "string",
          price: 0,
          expired_date: "2021-06-26T12:12:48.117000",
          image_url: "string",
          quantity: 0,
          category_id: null,
          stock: true,
          id: 18,
          is_active: true,
        },
      ],
      customers: [],
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
    // this.getListItem();
  },
  methods: {
    initialize() {},
    getListItem() {
      axios.get("/api/v1/items/all?skip=0&limit=100").then((data) => {
        this.items = data.data;
        console.log(data.data);
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
      this.editedIndex = this.orderItems.indexOf(item);
      this.showDialogDelete = true;
    },
    deleteItemConfirm() {
      this.orderItems.splice(this.editedIndex, 1);
      this.closeDelete();
      this.caculateTotalPrice();
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
    },
    closePayDialog() {
      this.showPayDialog = false;
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
</style>