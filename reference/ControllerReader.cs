using UnityEngine;
using UnityEngine.XR;

public class ControllerReader : MonoBehaviour
{
    void Update()
    {
        var right = InputDevices.GetDeviceAtXRNode(
            XRNode.RightHand
        );

        if (!right.isValid)
            return;

        bool hasPos = right.TryGetFeatureValue(
            CommonUsages.devicePosition,
            out Vector3 position
        );

        bool hasRot = right.TryGetFeatureValue(
            CommonUsages.deviceRotation,
            out Quaternion rotation
        );

        bool hasTrigger = right.TryGetFeatureValue(
            CommonUsages.trigger,
            out float trigger
        );

        if (hasPos && hasRot)
        {
            Debug.Log(
                $"Position: {position}, " +
                $"Rotation: {rotation}, " +
                $"Trigger: {(hasTrigger ? trigger : 0f)}"
            );
        }
    }
}
