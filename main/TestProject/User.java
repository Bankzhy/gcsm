import java.util.ArrayList;

public class User {
    private String userName;
    private String userGender;
    private String userTable="user";
    private DBConnection dbConnection = new DBConnection();
    private ArrayList<Item> cartItemList = new ArrayList<Item>();

    public String getUserName() {return userName;}
    public void setUserName(String userName) { this.userName = userName;}

    public String getUserGender() { return userGender; }
    public void setUserGender(String userGender) { this.userGender = userGender; }

    public void createUser() {
        if (this.userName != null && this.userGender != null) {
            if (checkUserNameExist()) {
                System.out.println("user created failed");
            } else {
                this.insertUserTable();
            }
        } else {
            System.out.println("user created failed");
        }
    }
    public void updateUserName(String newName) {
        if (checkUserNameExist()) {
            System.out.println("user update failed");
        } else {
            this.userName = newName;
            this.updateUserTable();
        }
    }

    private void insertUserTable() {
        if (checkUserNameExist()) {
            System.out.println("user created failed");
        } else {
            String query = "insert into" + this.userTable + "values" + this.userName + this.userGender;
            dbConnection.excute(query);
        }
    }

    private void updateUserTable() {
        String query = "update" + this.userTable + "values" + this.userName + this.userGender;
        dbConnection.excute(query);
    }

    private boolean checkUserNameExist() {
        String query = "select * from" + this.userTable + "where user_name = " + this.userName;
        dbConnection.excute(query);
        return true;
    }

    public void addCartItem(Item item) {
        this.cartItemList.add(item);
    }

    public void removeCartItem(Item item) {
        this.cartItemList.remove(item);
    }

    public Integer getCurrentCartPrice() {
        Integer price = 0;
        for (int i = 0; i < this.cartItemList.size(); i++) {
            price += this.cartItemList.get(i).price;
        }
        return price;
    }
}
