import React from 'react';
import { BrowserRouter as Router, Routes, Route, createBrowserRouter, RouterProvider } from 'react-router-dom';
import Login from '../pages/Login';
import Register from '../pages/Register';
import HomeLayout from '../pages/HomeLayout';
import Landing from '../pages/Landing';
import LandingV2 from '../pages/LandingV2';
import Products from '../pages/Products';
import CreateProduct from '../pages/CreateProduct';
import EditProduct from '../pages/EditProduct';
import Categories from '../pages/Categories';
import CreateCategory from '../pages/CreateCategory';
import EditCategory from '../pages/EditCategory';
import Orders from '../pages/Orders';
import Jobs from '../pages/Jobs';
import CreateOrder from '../pages/CreateOrder';
import EditOrder from '../pages/EditOrder';
import ViewJobStatus from '../pages/ViewJobStatus';
import Reviews from '../pages/Reviews';
import EditReview from '../pages/EditReview';
import CreateReview from '../pages/CreateReview';
import Users from '../pages/Users';
import EditUser from '../pages/EditUser';
import CreateUser from '../pages/CreateUser';
import HelpDesk from '../pages/HelpDesk';
import Notifications from '../pages/Notifications';
import Profile from '../pages/Profile';


const router = createBrowserRouter([
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/register",
    element: <Register />,
  },
  {
    path: "/",
    element: <HomeLayout />,
    children: [
      {
        index: true,
        element: <Landing />,
      },
      {
        path: "landing-v2",
        element: <LandingV2 />,
      },
      {
        path: "products",
        element: <Products />,
      },
      {
        path: "products/create-product",
        element: <CreateProduct />,
      },
      {
        path: "products/:id",
        element: <EditProduct />,
      },
      {
        path: "categories",
        element: <Categories />,
      },
      {
        path: "categories/create-category",
        element: <CreateCategory />,
      },
      {
        path: "categories/:id",
        element: <EditCategory />,
      },
      {
        path: "orders",
        element: <Orders />,
      },
      {
        path: "jobs",
        element: <Jobs />,
      },
      {
        path: "orders/create-order",
        element: <CreateOrder />,
      },
      {
        path: "orders/1",
        element: <EditOrder />,
      },
      {
        path: "job-status",
        element: <ViewJobStatus />
      },
      {
        path: "reviews",
        element: <Reviews />,
      },
      {
        path: "reviews/:id",
        element: <EditReview />,
      },
      {
        path: "reviews/create-review",
        element: <CreateReview />,
      },
      {
        path: "users",
        element: <Users />,
      },
      {
        path: "users/:id",
        element: <EditUser />,
      },
      {
        path: "users/create-user",
        element: <CreateUser />,
      },
      {
        path: "help-desk",
        element: <HelpDesk />,
      },
      {
        path: "notifications",
        element: <Notifications />,
      },
      {
        path: "profile",
        element: <Profile />,
      }
    ],
  },
]);

const HealthAppRouter = () => {
  return <RouterProvider router={router} />
}

  export default HealthAppRouter;