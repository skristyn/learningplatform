export const getRequest = <T>(path: string, token: string): Promise<T> => {
  const url = process.env.VUE_APP_API_URL + "/api/v1/" + path;

  const headers = new Headers({
    Authorization: `Token ${token}`,
  });

  return fetch(url, {
    method: "GET",
    headers: headers,
  }).then((response) => response.json());
};

export const postRequest = <T>(
  path: string,
  body: Record<string, unknown>,
  token: string
): Promise<T> => {
  const url = process.env.VUE_APP_API_URL + "/api/v1/" + path;

  const headers = new Headers({
    Authorization: `Token ${token}`,
  });

  return fetch(url, {
    method: "POST",
    body: JSON.stringify(body),
    headers: headers,
  }).then((response) => response.json());
};

export const getToken = (
  username: string,
  password: string
): Promise<{ token: string }> => {
  // define path to get the token
  const url = process.env.VUE_APP_API_URL + "/api/v1/token-auth";
  const formData = new FormData();
  formData.append("username", username);
  formData.append("password", password);

  return fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" }, // have to say what format of data  you're sending
    body: JSON.stringify({ username, password }), // this is the data you're sending
  }).then((response) => response.json());
};
