using UnityEngine;

public class AnimationEventReceiver : MonoBehaviour
{
	private byte handTag;

	[SerializeField]
	private SO_FxGroup[] effects;

	[SerializeField]
	private ParticleSystem[] ptcSystems;

	private Model mdl;

	public bool isHand => false;

	private void Awake()
	{
	}

	private void PlaySound(string input)
	{
	}

	private void AE_ReloadOver()
	{
	}

	private void KnifeAttack(int index)
	{
	}

	private void BulletRelease()
	{
	}

	private void PlayEffect(int index)
	{
	}

	private void WeaponSpecialEvent(string msg)
	{
	}

	private void EffectSwitchEvent(string eventName)
	{
	}

	private void FootStep(int isRightFoot)
	{
	}

	private void JumpEvent(int isDrop)
	{
	}
}
