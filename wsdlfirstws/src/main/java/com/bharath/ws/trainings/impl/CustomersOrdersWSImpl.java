package com.bharath.ws.trainings.impl;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.bharath.ws.trainings.CreateOrdersRequest;
import com.bharath.ws.trainings.CreateOrdersResponse;
import com.bharath.ws.trainings.CustomerOrdersPortType;
import com.bharath.ws.trainings.DeleteOrdersRequest;
import com.bharath.ws.trainings.DeleteOrdersResponse;
import com.bharath.ws.trainings.GetOrdersRequest;
import com.bharath.ws.trainings.GetOrdersResponse;
import com.bharath.ws.trainings.Order;
import com.bharath.ws.trainings.Product;

public class CustomersOrdersWSImpl implements CustomerOrdersPortType {

	Map<BigInteger, List<Order>> customerOrders = new HashMap<>();
	int currentCustomerId;

	public CustomersOrdersWSImpl() {
		init();
	}

	public void init() {
		List<Order> orders = new ArrayList<Order>();
		Order order = new Order();
		order.setId(BigInteger.valueOf(1));
		Product product = new Product();
		product.setDescription("IPhone");
		product.setId("1");
		product.setQuantity(BigInteger.valueOf(3));

		order.getProduct().add(product);

		orders.add(order);
		customerOrders.put(BigInteger.valueOf(++currentCustomerId), orders);
	}

	@Override
	public GetOrdersResponse getOrders(GetOrdersRequest request) {
		BigInteger id = request.getCustomerId();
		GetOrdersResponse response = new GetOrdersResponse();
		if(customerOrders.containsKey(id)){
			 response.getOrder().addAll(customerOrders.get(id));
		}
		return response;
	}

	@Override
	public CreateOrdersResponse createOrders(CreateOrdersRequest request) {
        BigInteger id = request.getCustomerId();
        Order order = request.getOrder();
        CreateOrdersResponse response = new CreateOrdersResponse();
        if(customerOrders.containsKey(id)){
            List<Order> ordersList = customerOrders.get(id);
            if(!ordersList.contains(order)){
            	response.setResult(true);
            	ordersList.add(order);
            	return response;
            }
        }
        response.setResult(false);
		return response;
	}

	@Override
	public DeleteOrdersResponse deleteOrders(DeleteOrdersRequest request) {
		BigInteger id = request.getCustomerId();
        Order order = request.getOrder();
        DeleteOrdersResponse response = new DeleteOrdersResponse();
        if(customerOrders.containsKey(id)){
            List<Order> ordersList = customerOrders.get(id);
            if(ordersList.contains(order)){
            	response.setResult(true);
            	ordersList.remove(order);
            	return response;
            }
        }
        response.setResult(false);
		return response;
	}
	
}
