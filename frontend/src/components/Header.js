import React, { useState } from "react";
import {AppBar, Autocomplete, Box, Tab, Tabs, TextField, Toolbar} from '@mui/material';
import MovieIcon from '@mui/icons-material/Movie';
import "./Header.css";
import { Link } from "react-router-dom";

const dummyArray = ["Jathi Ratnalu", "Bahubali", "Vikram"]
const Header = () => {
    const [value, setValue] = useState(0);
    return <AppBar position="sticky" sx={{bgcolor: "#2b2d42" }}>
        <Toolbar>
           <Box width={'20%'}>
                <MovieIcon/>
           </Box>

           <Box width={'30%'} margin={"auto"}>
           <Autocomplete
                sx={{borderBottom: "1px solid white"}}
                freeSolo
                options={dummyArray.map((option) => option)}
                renderInput={(params) => (
                <TextField className="textfield" sx={{input:{color:"white"}}}
                variant="standard" {...params} placeholder="Search Across Multiple Movies" />)}
             />
           </Box>

            <Box display={"flex"}>
                <Tabs textColor="inherit" indicatorColor="secondary" value={value} onChange={(e, val)=>setValue(val)}>
                    <Tab LinkComponent={Link} to="/movies" label="Movies"/>
                    <Tab LinkComponent={Link} to="/admin" label="Admin"/>
                    <Tab LinkComponent={Link} to="/auth" label="Auth"/>
                </Tabs>
            </Box>

        </Toolbar>
    </AppBar>
};

export default Header;