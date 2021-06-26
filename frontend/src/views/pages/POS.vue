<template>
  <v-container class="grey lighten-5" fluid fill-height>
    <v-layout>
      <v-col lg="4">
        <v-card class="pa-2 h-min-85vh" outlined tile>
          <v-row>
            <v-col cols="9">
              <v-select
                :items="items"
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
              :items="items"
              :items-per-page="5"
              class="elevation-1 ma-5"
            ></v-data-table>
          </v-row>
        </v-card>
        <v-footer padless class="font-weight-medium fontsize-13">
          <v-col class="text-center" cols="12">
            <v-row>
              <v-col cols="6">
                <v-row>
                  <v-col cols="6"> Total Items(s) </v-col>
                  <v-col cols="6"> : 0 </v-col>
                </v-row>
              </v-col>
              <v-col cols="6">
                <v-row>
                  <v-col cols="6"> Price </v-col>
                  <v-col cols="6"> : $2.00 </v-col>
                </v-row>
                <v-row>
                  <v-col cols="6"> Gross Price (inc 0% Tax) </v-col>
                  <v-col cols="6"> : $2.00 </v-col>
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
            <v-card class="mr-2" @click="alert('123')">
              <v-img
                class="ma-3 rounded-circle"
                height="150"
                width="150"
                src="https://cdn.vuetifyjs.com/images/cards/cooking.png"
              ></v-img>

              <v-card-text
                class="font-weight-medium text-center text-subtitle-1 pa-0 mt-2"
              >
                Text
              </v-card-text>
              <v-divider class="mx-4"></v-divider>

              <v-card-text
                class="font-weight-medium text-center text-subtitle-1 pa-0 mt-2"
              >
                Cafe Badilico
              </v-card-text>

              <v-card-text
                class="font-weight-medium text-center text-subtitle-1 pa-0"
              >
                $ 123.00
              </v-card-text>
            </v-card>
          </v-row>
        </v-card>
      </v-col>
    </v-layout>
  </v-container>
</template>

<script>
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
      ],
      items: [
        {
          rownumber: 1,
          name: "Frozen Yogurt",
          quantity: 159,
          price: 6.0,
        },
        {
          rownumber: 2,
          name: "Frozen Yogurt",
          quantity: 130,
          price: 6.0,
        },
      ],
    };
  },
};
</script>


<style scoped>
.h-min-85vh {
  min-height: 65vh !important;
}
.fontsize-13{
    font-size: 13px !important;
}
</style>