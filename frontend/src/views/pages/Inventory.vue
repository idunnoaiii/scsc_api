<template>
  <v-layout>
    <v-row justify="center">
      <v-col cols="10">
        <v-data-table
          :headers="headers"
          :items="items"
          sort-by="name"
          class="elevation-1"
          width="90%"
          :search="search"
        >
          <template v-slot:[`item.description`]="{ item }">
            <!-- <span>{{ item.stock == true ? "Yes" : "No" }}</span> -->
            <v-img
              :src="
                item.image_url != null
                  ? item.image_url
                  : 'https://storage.googleapis.com/scscbakery.appspot.com/no-image.png'
              "
              max-height="50px"
              max-width="50px"
            />
          </template>
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title class="text-h4">Items</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-text-field
                v-model="search"
                label="Search"
                hide-details
                class="mx-4"
              ></v-text-field>
              <v-spacer></v-spacer>
              <v-dialog v-model="dialog" max-width="500px">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    color="primary"
                    dark
                    class="mb-2"
                    v-bind="attrs"
                    v-on="on"
                  >
                    New
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title>
                    <span class="text-h5">{{ formTitle }}</span>
                  </v-card-title>

                  <v-card-text>
                    <v-form ref="form" lazy-validation v-model="valid">
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="6" md="12">
                            <v-text-field
                              v-model="editedItem.name"
                              label="Name*"
                              :rules="[required('Name')]"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="12">
                            <v-text-field
                              v-model="editedItem.description"
                              label="Description"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="12">
                            <v-text-field
                              v-model="editedItem.price"
                              label="Price*"
                              type="Number"
                              min="0"
                              step="1000"
                              :rules="[required('Price'), minNumberValue(1000)]"
                            ></v-text-field>
                          </v-col>

                          <v-col cols="12">
                            <v-chip-group
                              column
                              multiple
                              active-class="primary--text"
                              v-model="editedItem.categories"
                            >
                              <v-chip
                                v-for="cate_all in categories_all"
                                :key="cate_all.id"
                                :value="cate_all.id"
                              >
                                {{ cate_all.name }}
                              </v-chip>
                            </v-chip-group>
                          </v-col>

                          <v-col cols="6">
                            <v-file-input
                              accept="image/*"
                              label="Image"
                              @change="onFileSelected"
                            ></v-file-input>
                          </v-col>
                          <v-col cols="6">
                            <v-img :src="editedItem.image_url"></v-img>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-form>
                    <small>*indicates required field</small>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="blue darken-1"
                      class="white--text"
                      @click="close"
                      text
                    >
                      Cancel
                    </v-btn>
                    <v-btn
                      color="green darken-1"
                      class="white--text"
                      @click="save"
                      :disabled="!valid"
                    >
                      Save
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
              <v-dialog v-model="dialogDelete" max-width="500px">
                <v-card>
                  <v-card-title class="text-h5"
                    >Are you sure you want to delete this item?</v-card-title
                  >
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="blue darken-1"
                      class="white--text"
                      @click="closeDelete"
                      text
                      >Cancel</v-btn
                    >
                    <v-btn
                      color="red darken-1"
                      class="white--text"
                      @click="deleteItemConfirm"
                      >OK</v-btn
                    >
                    <v-spacer></v-spacer>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <v-icon small class="mr-2" @click="editItem(item)">
              mdi-pencil
            </v-icon>
            <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
          </template>
          <template v-slot:no-data>
            <v-btn color="primary" @click="load"> Reset </v-btn>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-layout>
</template>
<script>
import axios from "../../axios";
export default {
  data: () => ({
    valid: true,
    dialog: false,
    password: "",
    search: "",
    dialogDelete: false,
    selectedFile: null,
    categories_all: [],
    categories_range: [],
    headers: [
      {
        text: "Name",
        align: "start",
        value: "name",
      },
      { text: "Image", value: "description", sortable: false  },
      { text: "Price", value: "price" },
      { text: "Action", value: "actions", sortable: false },
    ],
    items: [],
    editedIndex: -1,
    editedItem: {
      name: "",
      description: "",
      price: 0,
      expired_date: "",
      image_url: null,
      quantity: 0,
      categories: [],
      id: 0,
      is_active: false,
    },
    defaultItem: {
      full_name: "",
      username: "",
      role: "",
    },
    categorySelected: false,
    required(inputName) {
      return (v) =>
        (v && v.toString().length > 0) || `${inputName} is required.`;
    },
    noSpace() {
      return (v) => (v || "").indexOf(" ") < 0 || "No spaces are allowed";
    },
    minNumberValue(value) {
      return (v) => (v && v >= value) || `Must be greater than ${value}`;
    },
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Item" : "Edit Item";
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  // created() {
  //   this.initialize();
  // },

  mounted() {
    this.load();
  },
  methods: {
    load() {
      axios
        .get("api/v1/items/all?skip=0&limit=100")
        .then((response) => {
          this.items = response.data;
        })
        .catch((err) => {
          console.log(err);
        });

      axios.get("/api/v1/categories").then((response) => {
        this.categories_all = response.data.map((item) => ({
          name: item.name,
          id: item.id,
        }));
      });
    },

    onFileSelected(file) {
      this.selectedFile = file;
      if (file) {
        const fileReader = new FileReader();
        fileReader.addEventListener("load", () => {
          this.editedItem.image_url = fileReader.result;
        });
        fileReader.readAsDataURL(file);
      }
    },

    editItem(item) {
      this.editedIndex = this.items.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
      this.password = "";
    },

    deleteItem(item) {
      this.editedIndex = this.items.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      // this.items.splice(this.editedIndex, 1);
      axios
        .delete(`/api/v1/items/${this.editedItem.id}`)
        .then((response) => {
          if (response.status == 200) {
             this.$store.commit("SET_TOAST", {
              toastMsg: "Item deleted!",
              toastColor: "green",
            });
            this.load();
          }
        })
        .catch((err) => {
          console.log(err);
        });

      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.$refs.form.reset();
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      if (!this.$refs.form.validate()) {
        return;
      }

      const item_added = {
        name: this.editedItem.name,
        description: this.editedItem.description,
        price: this.editedItem.price,
        quantity: this.editedItem.quantity,
        categories: this.editedItem.categories,
      };

      if (this.editedIndex > -1) {
        // update
        let fd = new FormData();

        //if update action then add id to item for notice
        item_added.id = this.editedItem.id;

        let item_json = JSON.stringify(item_added);

        fd.append("data", item_json);

        if (this.selectedFile) {
          fd.append("image", this.selectedFile, this.selectedFile.name);
        }

        axios
          .put("/api/v1/items/update", fd)
          .then((response) => {
            if (response.status == 200) {
               this.$store.commit("SET_TOAST", {
              toastMsg: "Item updated!",
              toastColor: "green",
            });
              this.load();
            }
          })
          .catch((err) => {
            console.log(err);
          });
      } else {
        // insert

        let fd = new FormData();

        let item_json = JSON.stringify(item_added);

        fd.append("data", item_json);


        if (this.selectedFile) {
          fd.append("image", this.selectedFile, this.selectedFile.name);
        }

        axios.post("/api/v1/items/create", fd).then((response) => {
          if (response.status == 200) {
             this.$store.commit("SET_TOAST", {
              toastMsg: "Item added!",
              toastColor: "green",
            });
            this.load();
          }
        });
      }
      this.close();
    },

    filterUser(value, search, items) {
      console.log(items);
      return (
        value != null &&
        search != null &&
        typeof value === "string" &&
        value.toString().indexOf(search) !== -1
      );
    },
  },
};
</script>