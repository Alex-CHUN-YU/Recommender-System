package ml_model_client;

import java.io.BufferedInputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.io.BufferedOutputStream;

/**
 * Connect ML Model.
 */
public class SocketClient {
    /**
     * Result.
     */
    private String result = "error";
    /**
     * Connect to ML Server.
     * @param data data
     * @return result
     */
    public String connecting(String data) {
//        String address = "140.116.245.146";
        String address = "127.0.0.1";
        int port = 1994;
        Socket client = new Socket();
        InetSocketAddress isa = new InetSocketAddress(address, port);
        try {
            client.connect(isa, 10000);
            BufferedOutputStream out = new BufferedOutputStream(client
                    .getOutputStream());
            BufferedInputStream in = new BufferedInputStream(client
                    .getInputStream());
            // 送出字串
            out.write(data.getBytes("UTF-8"));
            out.flush();
            // 接收字串
            byte[] buffer = new byte[1024]; // a read buffer of 5KiB
            int red = client.getInputStream().read(buffer);
            byte[] redData = new byte[red];
            System.arraycopy(buffer, 0, redData, 0, red);
            result = new String(redData,"UTF-8"); // assumption that client sends data UTF-8 encoded
            out.close();
            client.close();
        } catch (java.io.IOException e) {
            System.out.println("Socket連線有問題 !");
            System.out.println("IOException :" + e.toString());
        }
        return result;
    }
    /**
     * Test
     * @param args system default
     */
    public static void main(String[] args) {
        SocketClient socketClient = new SocketClient();
        System.out.println(socketClient.connecting("警察 女兒 @所作所為 爸爸 @職位 警察 兄弟@ 姐妹 表現@ 姐姐 妹妹 黑鍋 警察 身 & 所作所為 爸爸"));
    }
}