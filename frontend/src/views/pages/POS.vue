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
              <v-btn elevation="0" small class="rounded-5" color="#81c868">
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
      <v-dialog v-model="dialogDelete" max-width="500px">
        <v-card>
          <v-card-title class="text-h5"
            >Are you sure you want to delete this item?</v-card-title
          >
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="closeDelete"
              >Cancel</v-btn
            >
            <v-btn color="blue darken-1" text @click="deleteItemConfirm"
              >OK</v-btn
            >
            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>
  </v-container>
</template>

<script>
import axios from "../../axios";
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
      orderItems: [],
      items: [],
      customers: [],
      totalItem: 0,
      totalPrice: 0,
      grossPrice: 0,
      tax: 10,
      dialogDelete: false,
      defaultItem: {},
      editedIndex: 0,
    };
  },
  mounted() {
    this.getListItem();
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
        item.rownumber = index +1;
        totalItem += item.quantity;
        totalPrice += item.quantity * item.price;
      }

      this.totalItem = totalItem;
      this.totalPrice = totalPrice;
      this.grossPrice = totalPrice;
    },
    deleteItem(item) {
      this.editedIndex = this.orderItems.indexOf(item);
      this.dialogDelete = true;
    },
    deleteItemConfirm() {
      this.orderItems.splice(this.editedIndex, 1);
      this.closeDelete();
      this.caculateTotalPrice();
    },
    closeDelete() {
      this.dialogDelete = false;
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