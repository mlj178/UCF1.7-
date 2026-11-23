using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class HUD_NanoDamageScore : Singleton<HUD_NanoDamageScore>
{
	private int maxDamage;

	[SerializeField]
	private RectTransform[] starRect;

	[SerializeField]
	private RawImage[] starImage;

	[SerializeField]
	private GameObject damageStarPrefab;

	[SerializeField]
	private RectTransform damageStarBornPos;

	private SimpleObjectPool starPool;

	[SerializeField]
	private GameObject goalStarPrefab;

	private SimpleObjectPool goalStarPool;

	[SerializeField]
	private RectTransform[] forStarEffect;

	private float randomDistance;

	private float nextGoalFxTime;

	private int nextStarPos;

	private Queue<bool> starQueue;

	private static readonly float shrinkAnimTime;

	public static Action activeStarRecycyle;

	public static Action goalStarRecycle;

	[SerializeField]
	private CommonKillMark nanoScore;

	[SerializeField]
	private Texture scoreMark;

	[SerializeField]
	private AnimationHud nanoKillMark;

	protected override void Awake()
	{
	}

	private void Start()
	{
	}

	private void OnMyPlayerJoin(Player myPlayer)
	{
	}

	private void OnMyPlayerLifeStateChange(bool alive)
	{
	}

	private void OnMyPlayerTeamChange(Team newTeam)
	{
	}

	public override void SetVisible(bool newVisbile)
	{
	}

	protected override void OnDestroy()
	{
	}

	public void ResetStar()
	{
	}

	private void DamageEvent(ref DamageEventData eventData)
	{
	}

	private void AddStartCount(int count, bool hide)
	{
	}

	private bool SubStarCount(int count)
	{
		return false;
	}

	private IEnumerator StarGenerator()
	{
		return null;
	}

	private void GenerateGoalStarEffect()
	{
	}

	public void StarArrive(int index, bool is500)
	{
	}

	public static void PlayNanoScoreMark(Texture tex)
	{
	}

	private void PlayNanoScoreMark()
	{
	}

	private void OnPlayNanoKillMark(bool oldState, bool newState)
	{
	}
}
