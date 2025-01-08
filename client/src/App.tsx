import { RouterProvider, createBrowserRouter, Navigate } from "react-router-dom";
import { ApiProvider } from './context/ApiProvider';
import { AiPocProvider } from "./AiPoc/context/AiPocProvider";
import HealthAppRouter from "./router/HealthAppRouter";
import AiPocRouter from "./AiPoc/router/AiPocRouter";

import {
  useConfig
} from './hooks'


// const router = createBrowserRouter([

//   {
//     path: "/login",
//     element: <Login />,
//   },
//   {
//     path: "/register",
//     element: <Register />,
//   },
//   {
//     path: "/",
//     element: <HomeLayout />,
//     children: [
//       {
//         index: true,
//         element: <Landing />,
//       },
//       {
//         path: "/landing-v2",
//         element: <LandingV2 />,
//       },
//       {
//         path: "/products",
//         element: <Products />,
//       },
//       {
//         path: "/products/create-product",
//         element: <CreateProduct />,
//       },
//       {
//         path: "/products/:id",
//         element: <EditProduct />,
//       },
//       {
//         path: "/categories",
//         element: <Categories />,
//       },
//       {
//         path: "/categories/create-category",
//         element: <CreateCategory />,
//       },
//       {
//         path: "/categories/:id",
//         element: <EditCategory />,
//       },
//       {
//         path: "/orders",
//         element: <Orders />,
//       },
//       {
//         path: "/jobs",
//         element: <Jobs />,
//       },
//       {
//         path: "/orders/create-order",
//         element: <CreateOrder />,
//       },
//       {
//         path: "/orders/1",
//         element: <EditOrder />,
//       },
//       {
//         path: "/job-status",
//         element: <ViewJobStatus />
//       },
//       {
//         path: "/reviews",
//         element: <Reviews />,
//       },
//       {
//         path: "/reviews/:id",
//         element: <EditReview />,
//       },
//       {
//         path: "/reviews/create-review",
//         element: <CreateReview />,
//       },
//       {
//         path: "/users",
//         element: <Users />,
//       },
//       {
//         path: "/users/:id",
//         element: <EditUser />,
//       },
//       {
//         path: "/users/create-user",
//         element: <CreateUser />,
//       },
//       {
//         path: "/help-desk",
//         element: <HelpDesk />,
//       },
//       {
//         path: "/notifications",
//         element: <Notifications />,
//       },
//       {
//         path: "/profile",
//         element: <Profile />,
//       },
//       {
//         path:'/aipoc_landing',
//         element: <LandingAIPoc />
//       },
//       {
//         path: "/aipoc_root1",
//         element: <Root1/>
//       },
//       {
//         path: "/aipoc_root2",
//         element: <Root2/>
//       }
//     ],
    
//   },
// ]);

const App = () => {
  const {config, loading, error} = useConfig("./config.json");

  if (loading) {
    return <div> Loading ... </div>
  }

  if (error)  {
    return <div> Error loading config : {error.message} </div>
  }

  let ApiProviderComponent;
  let RouterComponent;

  switch(config?.Mode) {
    case "AiPoc":
      ApiProviderComponent = AiPocProvider;
      RouterComponent = AiPocRouter
      break;
    case "HealthCare":
      ApiProviderComponent = ApiProvider;
      RouterComponent = HealthAppRouter;
      break;
    default:
      throw new Error(`Unknown mode : ${config?.Mode}` )
  }


  return (
    <ApiProviderComponent>
        <RouterComponent />
    </ApiProviderComponent>
  );
}


export default App;
