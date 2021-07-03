<template>
  <v-row justify="center">
    <v-dialog
      v-model="$store.state.POS.showBillDialog"
      max-width="300"
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary white--text darken-1" @click="dialog = false">
            Print
          </v-btn>
        </v-card-actions>
        <!-- <v-card-title class="text-h5">
          Use Google's location service?
        </v-card-title> -->
        <v-divider class="pa-2"></v-divider>
        <v-card-text>
          <div class="ticket">
            <!-- <img src="./logo.png" alt="Logo" /> -->
            <p class="centered">
              SCSC Bakery <br />
              Contact: 8888 8888 8888 <br />
              Address: New york
            </p>
            <table>
              <thead>
                <tr>
                  <th class="description">Description</th>
                  <th class="quantity">Q.</th>
                  <th class="price">$$</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="i in 5" v-bind:key="i">
                  <td class="description">ARDUINO UNO R3</td>
                  <td class="quantity">1.00</td>
                  <td class="price">$25.00</td>
                </tr>
              </tbody>
            </table>
            <p class="centered">
              Thanks for your purchase! <br />parzibyte.me/blog
            </p>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {
  data() {
    return {};
  },
};
</script>

<style scoped>

td,
th,
tr,
table {
    width: 250px;
    border-top: 1px solid black;
    border-collapse: collapse;
}

td.description,
th.description {
  width: 75px;
  max-width: 75px;
}

td.quantity,
th.quantity {
  width: 40px;
  max-width: 40px;
  word-break: break-all;
}

td.price,
th.price {
  width: 40px;
  max-width: 40px;
  word-break: break-all;
}

.centered {
  text-align: center;
  align-content: center;
}

.ticket {
  width: 250px;
  max-width: 250px;
}

img {
  max-width: inherit;
  width: inherit;
}

@media print {
  .hidden-print,
  .hidden-print * {
    display: none !important;
  }
}
</style>