using System;
using System.Runtime.CompilerServices;
using CustomEvent;
using UnityEngine;

public class CFAnimator : Model
{
	[SerializeField]
	private SO_AnimationLerpData animLerpData;

	protected bool changeMode;

	[CompilerGenerated]
	private Action<string, string> m_AnimEnd_Listener;

	[NonSerialized]
	public bool alwaysRunAnim;

	[CompilerGenerated]
	private RefString m_AnimName_Modifier;

	private Coroutine knifeStun;

	protected Animator characterAnimator => null;

	protected Animator handAnimator => null;

	public Animator animator { get; protected set; }

	public string currentAnimName { get; protected set; }

	public string currentAnimTag { get; protected set; }

	public string tempAnimName { get; protected set; }

	public bool isAnimEmptyTag => false;

	public bool isSelecting => false;

	public bool isReloading => false;

	public bool semiGunShooting => false;

	public event Action<string, string> AnimEnd_Listener
	{
		[CompilerGenerated]
		add
		{
		}
		[CompilerGenerated]
		remove
		{
		}
	}

	public event RefString AnimName_Modifier
	{
		[CompilerGenerated]
		add
		{
		}
		[CompilerGenerated]
		remove
		{
		}
	}

	protected virtual void Update()
	{
	}

	private float GetAnimLerpTime(string animName)
	{
		return 0f;
	}

	public void PlayAnim(string animName, string animTag, bool isLoopAnim, float offset)
	{
	}

	public void PlayAnimIfNotPlaying(string animName, string animTag, bool isLoopAnim = false)
	{
	}

	public void PlayTempAnim(string animName, bool isLoopAnim = false, bool cancelIfPlaying = true, float offset = 0f)
	{
	}

	public void PlayWeaponAnimWithSameTag(string animName)
	{
	}

	public void PlayWeaponAnim(string animName, string animTag)
	{
	}

	private void AnimationEndMessage(AnimatorStateInfo stateInfo)
	{
	}

	protected virtual void OnAnimationEnter(string animName, string animTag)
	{
	}

	protected virtual void OnAnimationEnd(string animName, string animTag)
	{
	}

	protected virtual void OnAnimationExit(string animName, string animTag)
	{
	}

	protected void UpdateRunAnimation()
	{
	}

	protected void SetFloat(string name, float value, bool character)
	{
	}

	protected void UpdateAnimator(float deltaTime)
	{
	}

	protected void AnimatorInit()
	{
	}

	protected void PlayKnifeHitStunAnim(bool isBigshot)
	{
	}

	public void ChangeCurAnimToTemp()
	{
	}

	protected string ModifyAnimName(string animName)
	{
		return null;
	}
}
