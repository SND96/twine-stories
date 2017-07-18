/**
 * @class Initial
 */

import React, {Component} from "react";
import {
    Text,
    View,
    StyleSheet,
    Button,
    TextInput,
} from "react-native";

// import {Button} from "apsl-react-native-button";
// import FontAwesomeIcon from "react-native-vector-icons/FontAwesome";
import {Hideo} from "react-native-textinput-effects";
import CommonStyle from "../styles/common.css";
import Database from "../firebase/database";
import DismissKeyboard from "dismissKeyboard";
import * as firebase from "firebase";

class Initial extends Component {

    constructor(props) {
        super(props);

        this.state = {
            uid: "",
            role: ""
        };
    }

  renderRow = (rowData) => {
    return (
      <View>
      <Text style={styles.row}>
        {rowData.text}
      </Text>

      </View>
    )
  }

    async logout() {

        try {

            await firebase.auth().signOut();

            this.props.navigator.push({
                name: "Login"
            })

        } catch (error) {
            console.log(error);
        }

    }

     async componentDidMount() {

        try {

            // Get User Credentials
             user =  firebase.auth().currentUser;

            // Listen for Mobile Changes
            Database.listenRole(user.uid, (curr_role) => {
                this.setState({
                    role: curr_role
                });
            });

            this.setState({
                uid: user.uid
            });

        } catch (error) {
            console.log(error);
        }

    }

    saveRole() {
            // Set Mobile

                Database.setRole(this.state.uid, this.state.role);
                DismissKeyboard();
        }


    render() {

        return (
          <Picker
  selectedValue={this.state.role}
  onValueChange={() => this.saveRole()} >
    <Picker.Item label="Owner" value="owner" />
    <Picker.Item label="Manager" value="manager" />
    <Picker.Item label="Employee" value="employee" />
    </Picker>


        );
    }
}

const styles = StyleSheet.create({

    heading: {
        textAlign: "center"
    },

    logout: {
        padding: 50
    },

    form: {
        paddingTop: 50
    }

});

module.exports = Initial;
