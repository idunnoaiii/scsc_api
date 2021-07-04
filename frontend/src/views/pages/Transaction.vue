<template>
  <v-layout>
    <v-col cols="8" md="8">
      <v-card outlined height="100%">
        <v-container class="mt-5" flat>
          <v-row>
            <v-spacer></v-spacer>
            <v-md-date-range-picker class="my-2"></v-md-date-range-picker>
          </v-row>
        </v-container>

        <v-container fluid width="100%" class="mt-5">
          <v-row>
            <v-col cols="12" sm="4">
              <v-hover v-slot="{ hover }" open-delay="200">
                <v-card color="cyan darken-1" :elevation="hover ? 16 : 2">
                  <v-row>
                    <v-col cols="12" sm="8">
                      <v-list-item three-line>
                        <v-list-item-content>
                          <div class="mb-4">
                            <v-btn fab color="cyan" elevation="0">
                              <v-icon color="white">fab fa-bitcoin</v-icon>
                            </v-btn>
                          </div>
                          <v-list-item-title class="headline md-1 white--text">
                            $1000
                          </v-list-item-title>
                          <v-list-item-subtitle class="white--text">
                            Market Cap $151.458
                          </v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                    </v-col>
                    <v-col cols="12" sm="4">
                      <!-- <v-avatar size="100" class="ml-n10 mt-6"> -->
                      <div
                        size="100"
                        class="text-h1 text-center white--text mt-6 ml-n15"
                      >
                        15
                      </div>
                      <!-- </v-avatar> -->
                    </v-col>
                  </v-row>
                </v-card>
              </v-hover>
            </v-col>
            <v-col cols="12" sm="4">
              <v-hover v-slot="{ hover }" open-delay="200">
                <v-card color="pink darken-1" :elevation="hover ? 16 : 2">
                  <v-row>
                    <v-col cols="12" sm="8">
                      <v-list-item three-line>
                        <v-list-item-content>
                          <div class="mb-4">
                            <v-btn fab color="pink lighten-2" elevation="0">
                              <v-icon color="white"> fas fa-rupee-sign</v-icon>
                            </v-btn>
                          </div>
                          <v-list-item-title class="headline mb-1 white--text">
                            $12000
                          </v-list-item-title>
                          <v-list-item-subtitle class="white--text">
                            Market Cap $151.458
                          </v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                    </v-col>
                    <v-col cols="12" sm="4">
                      <!-- <v-avatar size="100" class="ml-n10 mt-6"> -->
                      <div
                        size="100"
                        class="text-h1 text-center white--text mt-6 ml-n15"
                      >
                        15
                      </div>
                      <!-- </v-avatar> -->
                    </v-col>
                  </v-row>
                </v-card>
              </v-hover>
            </v-col>
            <v-col cols="12" sm="4">
              <v-hover v-slot="{ hover }" open-delay="200">
                <v-card color="orange darken-1" :elevation="hover ? 16 : 2">
                  <v-row>
                    <v-col cols="12" sm="8">
                      <v-list-item three-line>
                        <v-list-item-content>
                          <div class="mb-4">
                            <v-btn fab color="orange lighten-2" elevation="0">
                              <v-icon color="white"> fas fa-rupee-sign</v-icon>
                            </v-btn>
                          </div>
                          <v-list-item-title class="headline mb-1 white--text">
                            $12000
                          </v-list-item-title>
                          <v-list-item-subtitle class="white--text">
                            Market Cap $151.458
                          </v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                    </v-col>
                    <v-col cols="12" sm="4">
                      <!-- <v-avatar size="100" class="ml-n10 mt-6"> -->
                      <div
                        size="100"
                        class="text-h1 text-center white--text mt-6 ml-n15"
                      >
                        15
                      </div>
                      <!-- </v-avatar> -->
                    </v-col>
                  </v-row>
                </v-card>
              </v-hover>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-sheet elevation="2">
                <v-card-title>
                  Orders
                  <v-spacer></v-spacer>
                  <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                  ></v-text-field>
                </v-card-title>
                <v-data-table
                  :headers="orderHeaders"
                  :items="orders"
                  :search="search"
                  @click:row="handleClick"
                >
                  <template v-slot:[`item.created_date`]="{ item }">
                    <span>{{ item.created_date | toMoment }}</span>
                  </template>
                </v-data-table>
              </v-sheet>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-col>
    <v-col cols="4" md="4">
      <v-card outlined height="100%">
        <v-list-item three-line>
          <v-list-item-content>
            <v-list-item-title class="text-h5 mb-1"> Orders </v-list-item-title>
            <v-sheet elevation="2">
              <v-data-table
                :headers="orderItemHeaders"
                :items="orderItems"
                :search="search"
                @click:row="handleClick"
              >
                <template v-slot:[`item.created_date`]="{ item }">
                  <span>{{ item.created_date | toMoment }}</span>
                </template>
              </v-data-table>
            </v-sheet>
          </v-list-item-content>
        </v-list-item>
      </v-card>
    </v-col>
  </v-layout>
</template>


<script>
import axios from "../../axios";
import moment from "moment";

export default {
  data() {
    return {
      dateRange: [],
      search: "",
      orderHeaders: [
        {
          text: "Code",
          align: "start",
          sortable: true,
          value: "code",
        },
        { text: "Date", value: "created_date" },
        { text: "Total", value: "subtotal" },
        { text: "Paid", value: "paid" },
        { text: "Change", value: "change" },
        { text: "Customer", value: "customer.name" },
        { text: "Cashier", value: "user.username" },
      ],
      orderItemHeaders: [
        { text:"Name", value: "item_name"},
        { text:"Quantity", value: "quantity"},
        { text:"Price", value: "price"}
      ],
      orders: [
        {
          customer_id: null,
          code: 0,
          user_id: 1,
          status: true,
          tax: 0,
          subtotal: 165000,
          paid: 500000,
          change: 499877,
          order_items: [
            {
              order_id: 30,
              item_id: 1,
              price: 20000,
              quantity: 3,
              item_name: "Bánh chuối tròn",
            },
            {
              order_id: 30,
              item_id: 9,
              price: 15000,
              quantity: 2,
              item_name: "Bánh Su kem",
            },
            {
              order_id: 30,
              item_id: 10,
              price: 10000,
              quantity: 2,
              item_name: "Bánh xúc xích phô mai",
            },
            {
              order_id: 30,
              item_id: 13,
              price: 25000,
              quantity: 1,
              item_name: "Bánh mì táo đỏ",
            },
            {
              order_id: 30,
              item_id: 11,
              price: 30000,
              quantity: 1,
              item_name: "Bánh mi hạt sen",
            },
          ],
        },
      ],
      orderItems: [

      ]
    };
  },
  created() {
    this.init();
    console.log(
      moment("2021-06-27T03:32:14.693000").format("MMMM Do YYYY, h:mm:ss a")
    );
  },
  methods: {
    init: function () {
      axios.get("/api/v1/orders/all?skip=0&limit=100").then((response) => {
        this.orders = response.data;
      });
    },
    handleClick(row) {
      this.orderItems = row.order_items;
    },
  },

  filters: {
    toMoment: function (date) {
      return moment(date).format("MM/DD/YYYY, h:mm a");
    },
  },
};
</script>