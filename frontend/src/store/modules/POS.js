import axios from '../../axios'

const state = () => ({
	orderItems: [],
	customer_checkout: null,
	totalItem: 0,
	totalPay: 0,
	discount: {
		threshold: 0,
		type: 0,
		value: 0
	},
	checkoutStatus: null,
	showBillDialog: false,
	customers: [
		{ text: "Walk-in customer", value: 0 }
	],
	customerValue: 0,
	tabs: [
		{
			orderItem: [],
			customer: null,
		}
	],
	listOnHold: [
		{
			value: 1,
			text: "Order 1",
		},
	],
	currentTab: 1,
	currentOrderCode: "",
})

const getters = {
	totalOrderItem(state) {
		return state.orderItems.reduce((acc, item) => acc + item.quantity, 0)
	},
	totalPrice(state) {
		return state.orderItems.reduce((acc, item) => acc + (item.quantity * item.price), 0)
	},
	discount(state) {
		return state.discount;
	},
	getCustomerCheckout(state) {
		return state.customers.filter(c => c.value == state.customerValue)[0];
	}
}

const actions = {
	checkout({ commit, state, getters, rootState }, payload) {



		let orderDetail = {
			code: state.currentOrderCode,
			user_id: rootState.userid,
			status: true,
			tax: 0,
			subtotal: getters.totalPrice - payload.discountValue,
			total: getters.totalPrice,
			discount: payload.discountValue,
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

		if (state.customerValue > 0) {
			orderDetail.customer_id = state.customerValue
		}

		orderDetail.order_items = state.orderItems.map((item) => ({
			item_id: item.id,
			price: item.price,
			quantity: item.quantity,
			item_name: item.name,
		}));

		axios
			.post("/api/v1/orders/", orderDetail)
			.then(() => {
				commit('CLEAR_ORDER_ITEM')
				commit('SET_PAYDIALOG', false, { root: true })
				commit('SET_TOAST', {
					toastMsg: "Checkout successfully",
					toastColor: "success"
				}, { root: true })
				commit('SET_ORDER_CODE')
			})
			.catch((err) => {
				console.log(err);
				commit('SET_CHECKOUT_STATUS', false)
			})
			.finally(() => {
				commit('SET_SELECTED_CUSTOMER', 0)
			});

	},

	getCustomer({ commit }) {
		axios.get("/api/v1/customers")
			.then((response) => {
				if (response.data) {
					const customers = response.data.map((item) => ({
						text: `${item.name} - ${item.contact}`,
						value: item.id,
					}));
					commit('SET_CUSTOMERS', customers)
				}

			});
	},

	calculateDiscount({ getters, commit }) {
		axios.get(`/api/v1/discounts/calculate/${getters.totalPrice}`)
			.then(response => {
				commit("SET_DISCOUNT", response.data)
			})
	},

	updateCurrentTab({ commit }, payload) {
		commit('SET_CURRENT_TAB', payload)
	},

	changeCustomerValue({ commit }, payload) {
		console.log(payload);
		commit('SET_SELECTED_CUSTOMER', payload)
	},

	addCusomterInPOS({ commit }, payload) {
		axios.get("/api/v1/customers")
			.then((response) => {
				if (response.data) {
					const customers = response.data.map((item) => ({
						text: `${item.name} - ${item.contact}`,
						value: item.id,
					}));
					commit('SET_CUSTOMERS', customers)
					commit('SET_SELECTED_CUSTOMER', payload)
				}

			});
	}

}

const mutations = {
	ADD_ITEM_TO_ORDER(state, item) {
		let itemIndex = state.orderItems.findIndex(x => x.id == item.id);
		if (itemIndex > -1) {
			state.orderItems[itemIndex].quantity++;
			return
		}
		let orderItem = {
			id: item.id,
			rownumber: state.orderItems.length + 1,
			name: item.name,
			quantity: 1,
			price: item.price,
		};
		state.orderItems.push(orderItem)
	},

	SET_CHECKOUT_STATUS(state, status) {
		state.checkoutStatus = status;
	},

	SET_ORDER_CODE(state) {
		console.log("SET_ORDER_CODE")
		state.currentOrderCode = new Date().getTime()
	},

	INCREASE_ITEM_QUANTITY(state, id) {
		let item = state.orderItems.find(x => x.id == id)
		if (item) item.quantity++
	},

	DECREASE_ITEM_QUANTITY(state, id) {
		let item = state.orderItems.find(x => x.id == id)
		if (item == null || item == undefined)
			return;
		if (item.quantity > 1) {
			item.quantity--;
			return;
		}
		state.orderItems = state.orderItems.filter(x => x.id != id);
	},

	CLEAR_ORDER_ITEM(state) {
		state.orderItems = [];
	},

	SET_BILL_DIALOG(state, status) {
		state.showBillDialog = status;
	},

	SET_CURRENT_TAB(state, payload) {
		state.currentTab = payload;
	},

	CLEAR_CHECKOUT_DATA(state) {
		state.orderItems = [];
	},

	DELETE_ITEM_ORDER(state, id) {
		state.orderItems = state.orderItems.filter(x => x.id != id);
	},

	SET_CUSTOMERS(state, payload) {
		state.customers.push(...payload);
		console.log(state.customers)
	},

	SET_DISCOUNT(state, payload) {
		state.discount = payload
	},

	UPDATE_ITEM_QUANTITY(state, payload) {
		console.log("UPDATE_ITEM_QUANTITY", payload)
		state.orderItems.find(x => x.id == payload.itemId).quantity = parseInt(payload.quantity);
	},

	SET_SELECTED_CUSTOMER(state, payload) {
		state.customerValue = payload
	},

	REMOVE_ON_HOLD(state, payload) {
		if (state.listOnHold.length == 1) return;
		state.listOnHold = state.listOnHold.reduce((acc, item) => {
			if (item.value != payload) {
				acc.push(item);
			}
			return acc;
		}, []);
	},

	ADD_ON_HOLD(state) {
		let len = state.listOnHold.length;
		if (len == 20) return;
		let max = state.listOnHold.reduce((acc, item) => {
			if (item.value > acc) {
				acc = item.value;
				return acc;
			}
		}, 0);
		state.listOnHold.push({ value: max + 1, text: `Order ${max + 1}` });
		state.currentTab = max + 1
	},

	BLUR_CUSTOMER(state) {
		if (state.customerValue == null)
			state.customerValue = state.customers[0]
	}

}


export default {
	namespaced: true,
	state,
	getters,
	actions,
	mutations
}