import React, { FunctionComponent } from "react";
import {FullPage, Slide} from 'react-full-page';
import LandingAIPoc from "./LandingAIPoc";
import Root1 from "./Root1";

export type MainPageType = {

};


const MainPage:FunctionComponent<MainPageType> = () => {


    return (
        <FullPage duration={1000}
                    controls>
            <Slide>
                <LandingAIPoc></LandingAIPoc>
            </Slide>
            <Slide>
                <Root1></Root1>
            </Slide>
        </FullPage>
    );

}

export default MainPage;