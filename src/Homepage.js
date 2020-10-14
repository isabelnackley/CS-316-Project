import React from "react";
import "./Home.css";
import Product from "./Product";

function Home() {
  return (
    <div className="home">
      <div className="home__container">
        <div className="home__row">
          <Product
            id="1"
            title="SQL Cookbook"
            price={47.96}
            rating={5}
            image="https://www.datapine.com/blog/wp-content/uploads/2016/11/sql-cookbook-by-anthony-molinaro.jpg"
          />
          <Product
            id="2"
            title="Duke Basketball Season Tickets"
            price={99974.99}
            rating={5}
            image="https://pbs.twimg.com/media/CcuSLBYWAAABllT.jpg:large"
          />
          <Product
            id="49538094"
            title="Amazon Fire TV Stick 4K"
            price={49.99}
            rating={4}
            image="https://images-na.ssl-images-amazon.com/images/I/61mAA2BB-FL._AC_SL1000_.jpg"
          />
        </div>

        <div className="home__row">
          <Product
            id="4903850"
            title="Fitbit"
            price={199.99}
            rating={3}
            image="https://images-na.ssl-images-amazon.com/images/I/71Swqqe7XAL._AC_SX466_.jpg"
          />
          <Product
            id="23445930"
            title="Amazon Echo (3rd generation) | Smart speaker with Alexa, Charcoal Fabric"
            price={98.99}
            rating={5}
            image="https://media.very.co.uk/i/very/P6LTG_SQ1_0000000071_CHARCOAL_SLf?$300x400_retinamobilex2$"
          />
          <Product
            id="3254354345"
            title="New Apple iPad Pro (12.9-inch, Wi-Fi, 128GB) - Silver (4th Generation)"
            price={598.99}
            rating={4}
            image="https://images-na.ssl-images-amazon.com/images/I/816ctt5WV5L._AC_SX385_.jpg"
          />
        </div>
      </div>
    </div>
  );
}

export default Home;