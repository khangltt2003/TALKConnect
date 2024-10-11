import { useState, useEffect, useContext } from "react";
import AuthContext from "./AuthContext";
import axios from "../src/axios";

const ProfileHook = () => {
  const { authTokens, logoutUser } = useContext(AuthContext);
  const [profile, setProfile] = useState(null);
  const [profileLoaded, setProfileLoaded] = useState(false);

  const getProfile = async () => {
    try {
      let response = await axios({
        method: "GET",
        url: `/user/profile/`,
        headers: {
          Authorization: "Bearer " + String(authTokens.access),
        },
      });
      setProfile(response.data);
      setProfileLoaded(true); // Indicates the profile fetch attempt was made
    } catch (error) {
      console.error("Cannot get user profile", error);
    }
  };

  useEffect(() => {
    if (authTokens) {
      getProfile();
    }
  }, [authTokens]);

  return { profile, profileLoaded };
};

export default ProfileHook;
