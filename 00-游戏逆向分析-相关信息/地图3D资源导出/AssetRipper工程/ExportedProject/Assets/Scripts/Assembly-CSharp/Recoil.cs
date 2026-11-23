using UnityEngine;

public class Recoil : MonoBehaviour
{
	public ShootPosture shootPosture;

	private PostureFloat perturbMin;

	private PostureFloat perturbMax;

	[HideInInspector]
	public Vector2 perturbChangeSpeed;

	private PostureFloat detailedReactYawShot;

	private PostureFloat detailedReactPitchShot;

	private float addYaw_Target;

	private float addPitch_Target;

	private PostureFloat fullReactYaw;

	private PostureFloat fullReactPitch;

	private SideReactDirect sideReactDirect;

	private int shotRepeatCount;

	private int oneShotRepeatCount;

	private int longOneShotRepeatCount;

	private int longOneShotRepeatCount_CrossHair;

	private PostureFloat detailPerturbShot;

	private AmmoRecoverAndDecay shotReactYaw;

	private AmmoRecoverAndDecay shotReactPitch;

	private bool mirror;

	private bool shoot;

	private float oneShotTime;

	private float previousOneShotTime;

	private float previousShotTime;

	private int shotCount_CrossHair;

	private float nextCircleRealSize;

	private float circleMinSize;

	private float nextCircleShotSize;

	private float lastTargetSize;

	private ChangeMovingRealSize changeMovingRealSize;

	private DelayOneShootData delayOneShootTime;

	private bool isKnife;

	private int byGunRotateDirection;

	public float addYaw { get; private set; }

	public float addPitch { get; private set; }

	public float reactRate => 0f;

	public void SetPerturb(PostureFloat min, PostureFloat max)
	{
	}

	public void SetDetailedReactShot(PostureFloat yaw, PostureFloat pitch)
	{
	}

	public void SetDetailPerturbShot(PostureFloat detailPerturb)
	{
	}

	public void SetSideReactDirect(SideReactDirect sideReactDirect)
	{
	}

	public void SetShotReact(AmmoRecoverAndDecay yaw, AmmoRecoverAndDecay pitch)
	{
	}

	public void SetChangeMovingRealSize(ChangeMovingRealSize changeMovingRealSize)
	{
	}

	public void SetFullReact(PostureFloat yaw, PostureFloat pitch)
	{
	}

	public void SetDelayOneShoot(DelayOneShootData data)
	{
	}

	public float GetCurrentPerturb()
	{
		return 0f;
	}

	private void Update()
	{
	}

	private void LateUpdate()
	{
	}

	public void TransformUpdate()
	{
	}

	private void UpdateAddYaw()
	{
	}

	private void UpdateAddPitch()
	{
	}

	public void OnGunShot()
	{
	}

	private void ShotRepeatCountAdd()
	{
	}

	private int ShotRepeatCountClamp(int input, int maxClip)
	{
		return 0;
	}

	private Vector3 SetDirect(Vector3 direct)
	{
		return default;
	}

	public Ray GetShootRay()
	{
		return default;
	}

	public Ray GetKnifeAttackRay()
	{
		return default;
	}

	public Vector2 GetCurrentRecoil()
	{
		return default;
	}

	public void ResetShotRepeatCount(bool allResetSwitch = false)
	{
	}

	private void CalcCircleSizeForNextFrame()
	{
	}

	private Vector3 CalculateWeaponPath(Quaternion rGunDir)
	{
		return default;
	}

	public void ResetCrossHairValue()
	{
	}

	private void UpdateCrossHair()
	{
	}

	private void SendTargetSizeInfo(float minSize, float realSize)
	{
	}
}
