package cn.fitrecipe.android.function;

import android.content.Context;
import android.widget.Toast;

import com.android.volley.Response;
import com.android.volley.VolleyError;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.List;

import cn.fitrecipe.android.FrApplication;
import cn.fitrecipe.android.Http.FrRequest;
import cn.fitrecipe.android.Http.FrServerConfig;
import cn.fitrecipe.android.Http.PostRequest;
import cn.fitrecipe.android.dao.FrDbHelper;
import cn.fitrecipe.android.entity.DatePlanItem;

/**
 * Created by wk on 2015/10/12.
 */
public class JoinPlanHelper {

    private Context context;

    public JoinPlanHelper(Context context) {
        this.context = context;
    }

    public void joinPersonalPlan(final CallBack callBack) throws JSONException {
        JSONObject params = new JSONObject();
        JSONArray dish = new JSONArray();
        List<DatePlanItem> items = FrDbHelper.getInstance(context).generateDatePlan();
        for(int i = 0; i < items.size(); i++) {
            JSONObject obj = new JSONObject();
            obj.put("type", i);
            JSONArray ingredient = new JSONArray();
            JSONArray recipe = new JSONArray();
            JSONObject obj1 = new JSONObject();
            obj1.put("id", 1);
            obj1.put("amount", 200);
            ingredient.put(obj1);
            obj.put("ingredient", ingredient);
            obj.put("recipe", recipe);
            dish.put(obj);
        }
        params.put("dish", dish);
        PostRequest request = new PostRequest(FrServerConfig.getUpdatePlanUrl(), FrApplication.getInstance().getToken(), params, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject res) {
                try {
                    setInUse(res.getJSONObject("data").getInt("id"), callBack);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError volleyError) {

            }
        });
        FrRequest.getInstance().request(request);
    }

    private void setInUse(int id, final CallBack callBack) throws JSONException {
        JSONObject params = new JSONObject();
        params.put("plan", id);
        params.put("joined_date", Common.getDate());
        PostRequest request = new PostRequest(FrServerConfig.getUpdatePlanUrl(), FrApplication.getInstance().getToken(), params, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject res) {
                if(res.has("data")) {
                    try {
                        if(res.getString("data").equals("ok"))
                            callBack.handle();
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError volleyError) {

            }
        });
        FrRequest.getInstance().request(request);
    }

    public interface CallBack {
         void handle();
    }
}
